# -*- coding: utf-8 -*-

# Copyright (c) 2021 Future Internet Consulting and Development Solutions S.L.

# This file is part of BAE NGSI Dataset plugin.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import os
import re
import jwt
import json
import requests
from requests.exceptions import HTTPError
import uuid

import time
from datetime import datetime, timedelta

from urllib.parse import urlparse
from urllib.parse import parse_qs

from base64 import urlsafe_b64encode, b64decode

from django.conf import settings

from wstore.asset_manager.resource_plugins.plugin import Plugin
from wstore.asset_manager.resource_plugins.plugin_error import PluginError

BAE_VC = os.getenv('BAE_PLUGIN_VC')

UNITS = [{
    'name': 'Api call',
    'description': 'The final price is calculated based on the number of calls made to the API'
}]

class VcTilService(Plugin):

    def on_post_product_spec_validation(self, provider, asset):

        # Check vc type 
        if 'vc_type' not in asset.meta_info:
            raise PluginError('Verifiable Credential type must be specified.')

        # Check role name 
        if 'role_names' not in asset.meta_info:
            raise PluginError('Name of the roles must be specified.')

        # Set expiration duration
        try:
            asset.meta_info['minutes'] = int(asset.meta_info['minutes'])
        except:
            asset.meta_info['minutes'] = 10080  # One week

        asset.save()

    def _append_string_charact(self, charact, name, description, value):
        charact.append({
                "name": name,
                "description": description,
                "valueType": "string",
                "configurable": False,
                "productSpecCharacteristicValue": [{
                    "valueType": "string",
                    "default": True,
                    "value": value,
                    "unitOfMeasure": "",
                    "valueFrom": "",
                    "valueTo": ""
                }]
            })

    def on_post_product_spec_attachment(self, asset, asset_t, product_spec):
        # Load meta data as characteristics
        prod_url = '{}/api/catalogManagement/v2/productSpecification/{}'.format(
            settings.CATALOG, asset.product_id)


        # Get the product
        try:
            charact = product_spec['productSpecCharacteristic']

            # Add vc type
            if asset.meta_info['vc_type']: 
                self._append_string_charact(charact, 
                "Verifiable Credential type",
                "Type of verifiable credentials that can be issued.",
                asset.meta_info['vc_type'])

            # Add role name
            if asset.meta_info['role_names']: 
                self._append_string_charact(charact, 
                "Role name",
                "(Comma seperated) List of assingable roles.",
                asset.meta_info['role_names'])
             
            resp = requests.patch(prod_url, json={
                'productSpecCharacteristic': charact
            }, verify=False)

            resp.raise_for_status()
        except:
            # This is a nice to have, but the product is already created
            pass

    def on_post_product_offering_validation(self, asset, product_offering):
        pass

    def _get_allowed_roles(self, roles_str, did):
        allowed_values = []

        # Loop over roles
        roles = roles_str.split(',')
        for i,r in enumerate(roles):
            # Append single entry per role
            allowed_values.append({
                "names": [r],
                "target": did
            })

            # Add all roles in one entry
            names = [r]
            for j in roles[:i]:
                names.append(j)
            for k in roles[i+1:]:
                names.append(k)
            allowed_values.append({
                "names": names,
                "target": did
            })
                
        return allowed_values

    def _get_create_issuer_payload(self, asset, order, valid_from, valid_to):

        issuer = {
            "did": (order.owner_organization.issuerDid),
            "credentials": [
                {
                    "validFor": {
                        "from": valid_from,
                        "to": valid_to
                    },
                    "credentialsType": asset.meta_info['vc_type'],
                    "claims": [
                        {
                            "name": "roles",
                            "allowedValues": self._get_allowed_roles(asset.meta_info['role_names'], asset.meta_info['provider_did'])
                        }
                    ]
                }
            ]
        }
        return issuer

    def _same_device_flow(self, til_endpoint, payload):
        # Will perform the samedevice flow to obtain an access token from the verifier/provider
        
        # Send request without header, should result in redirect to verifier
        issuer_response = requests.post(til_endpoint, json=payload, allow_redirects=False)
        try:
            issuer_response.raise_for_status()
        except HTTPError as e:
            print('HTTP  ERROR')
            print(e.request.body)
            print(e)
            print(e.response.text)
            raise PluginError('Error when sending request to /issuer endpoint')
            
        # Get redirect URL for samedevice flow
        if issuer_response.status_code != 302:
            print("ERROR: Did not receive redirect from {}".format(til_endpoint))
            raise PluginError('Did not receive 302 redirect from {}'.format(til_endpoint))
        samedevice_endpoint = issuer_response.headers.get('location')
        if not samedevice_endpoint:
            print("ERROR: Did not receive redirect location from {}".format(til_endpoint))
            raise PluginError("ERROR: Did not receive redirect from {}".format(til_endpoint))

        # Get verifier URI
        parsed_url = urlparse(samedevice_endpoint)
        verifier_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)

        # Get redirect URL from samedevice endpoint
        samedevice_response = requests.get(samedevice_endpoint, allow_redirects=False)
        try:
            samedevice_response.raise_for_status()
        except HTTPError as e:
            print('HTTP  ERROR')
            print(e.request.body)
            print(e)
            print(e.response.text)
            raise PluginError('Error when sending request to samedevice endpoint')

        if samedevice_response.status_code != 302:
            print("ERROR: Did not receive redirect from {}".format(samedevice_endpoint))
            raise PluginError('Did not receive 302 redirect from {}'.format(samedevice_endpoint))
        auth_request_url = samedevice_response.headers.get('location')
        if not auth_request_url:
            print("ERROR: Did not receive redirect location from {}".format(samedevice_endpoint))
            raise PluginError("ERROR: Did not receive redirect from {}".format(samedevice_endpoint))
        
        # Parse URL
        parsed_url = urlparse(auth_request_url)
        params = parse_qs(parsed_url.query)

        # Build VP token
        vc = json.loads(b64decode(BAE_VC))
        vp_token = {
            "@context": [
                "https://www.w3.org/2018/credentials/v1"
            ],
            "type": [
                "VerifiablePresentation"
            ],
            "verifiableCredential": [
                vc
            ],
            "id": str(uuid.uuid4()),
            "holder": "did:example:holder",
            "proof": {
                "type": "Ed25519Signature2018",
                "created": "2021-03-19T15:30:15Z",
            }
        }
        
        # Send authentication_response
        auth_response_endpoint = "{}api/v1/authentication_response".format(verifier_url)
        presentation_definition = {
            # TODO: Just a placeholder, implement presentation_definition
            'definition_id': "Example definition",
            'id': "Placeholder - not yet evaluated."
        }
        auth_params = {
            #'state': params['state'][0],
            'presentation_submission': urlsafe_b64encode(str(presentation_definition).encode('utf-8')).rstrip(b'='),
            'vp_token': urlsafe_b64encode(json.dumps(vp_token).encode('utf-8')).rstrip(b'=')
        }
        query_params = {
            'state': params['state'][0]
        }
        auth_response = requests.post(auth_response_endpoint, params=query_params, data=auth_params, allow_redirects=False)
        try:
            auth_response.raise_for_status()
        except HTTPError as e:
            print('HTTP  ERROR')
            print(e.request.body)
            print(e)
            print(e.response.text)
            raise PluginError('Error when sending request to authentication_response endpoint')

        # Parse received location header
        auth_response_url = auth_response.headers.get('location')
        parsed_url = urlparse(auth_response_url)
        auth_response_params = parse_qs(parsed_url.query)

        # Get access token JWT
        token_endpoint = "{}/token".format(verifier_url)
        token_params = {
            "grant_type": "authorization_code",
            "code": auth_response_params['code'][0],
            "redirect_uri": verifier_url
        }
        token_response = requests.post(token_endpoint, data=token_params)
        try:
            token_response.raise_for_status()
        except HTTPError as e:
            print('HTTP  ERROR')
            print(e.request.body)
            print(e)
            print(e.response.text)
            raise PluginError('Error when sending request to /token endpoint')

        token_data = token_response.json()
        if 'access_token' not in token_data:
            raise PluginError('No access token in response')

        return token_data['access_token']
        
    def on_product_suspension(self, asset, contract, order):
        # TODO: Implement PUT overwrite with expired or empty entry, or using DELETE
        pass

    def on_product_acquisition(self, asset, contract, order):

        # Build trusted issuer entry payload
        d_now = datetime.now()
        valid_from = d_now.strftime('%Y-%m-%dT%H:%M:%SZ')
        d_to = d_now + timedelta(minutes = asset.meta_info['minutes'])
        valid_to = d_to.strftime('%Y-%m-%dT%H:%M:%SZ')
        payload = self._get_create_issuer_payload(asset, order, valid_from, valid_to)

        # Get JWT access token from verifier via AS
        til_endpoint = asset.meta_info['trusted_issuer_endpoint']
        token = self._same_device_flow(til_endpoint, payload)
        
        # Create trusted issuer at TIL
        issuer_response = requests.post(til_endpoint, json=payload, allow_redirects=False, headers={
            'Authorization': 'Bearer ' + token
        })
        try:
            issuer_response.raise_for_status()
        except HTTPError as e:
            print('HTTP  ERROR')
            print(e.request.body)
            print(e)
            print(e.response.text)
            raise PluginError('Error when sending request to /issuer endpoint for creating issuer')

    def get_usage_specs(self):
        return UNITS

    def get_pending_accounting(self, asset, contract, order):
        return [], None
        
if __name__ == "__main__":
    plugin = VcTilService()
    plugin.on_product_acquisition(None, None, None)
