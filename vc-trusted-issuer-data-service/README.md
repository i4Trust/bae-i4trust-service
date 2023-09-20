# vc-trusted-issuer-data-service
BAE Plugin for services, using role-based verifiable credentials and creating entries 
at an EBSI compliant Trusted Issuer List.

## Usage

Create a zip from the contents of this directory:
```shell
zip bae-vc-trusted-issuer-service.zip package.json vc_til_service.py
```
Alternatively download the zip file created with the release here on GitHub.

Copy the zip file to the `/plugins` directory of your charging backend component and load the plugin:
```shell
./manage.py loadplugin plugins/bae-vc-trusted-issuer-service.zip
```



### Configuration

The BAE plugin requires a VC to be able to access the activation service of each possible 
service provider in the data space, that place offerings on the marketplace.

These should be provided as a Base64 encoded JSON with the structure described in the following:
```
{
	"<DID_Provider1>": {
		<VC_For_Provider1>
	},
	"<DID_Provider2>": {
		<VC_For_Provider2>
	}
}
```

The following snippet gives an example
```json
{
    "did:web:packetdelivery.dsba.fiware.dev:did": {
        "type": [
            "VerifiableCredential",
            "ActivationService"
        ],
        "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "https://w3id.org/security/suites/jws-2020/v1"
        ],
        "id": "urn:uuid:c7e7d4a1-7579-40a3-b418-59f6a9f2f6b1",
        "issuer": "did:web:marketplace.dsba.fiware.dev:did",
        "issuanceDate": "2023-06-07T07:45:06Z",
        "issued": "2023-06-07T07:45:06Z",
        "validFrom": "2023-06-07T07:45:06Z",
        "expirationDate": "2032-12-08T13:05:06Z",
        "credentialSchema": {
            "id": "https://raw.githubusercontent.com/FIWARE-Ops/i4trust-provider/main/docs/schema.json",
            "type": "FullJsonSchemaValidator2021"
        },
        "credentialSubject": {
            "id": "0b876000-36c7-47ed-b896-5b5ec163663a",
            "roles": [
                {
                    "names": [
                        "CREATE_ISSUER"
                    ],
                    "target": "did:web:packetdelivery.dsba.fiware.dev:did"
                }
            ],
            "email": "marketplace@mymail.com"
        },
        "proof": {
            "type": "JsonWebSignature2020",
            "creator": "did:web:marketplace.dsba.fiware.dev:did",
            "created": "2023-06-07T07:45:06Z",
            "verificationMethod": "did:web:marketplace.dsba.fiware.dev:did#6f4c1255f4a54090bc8ff7365b13a9b7",
            "jws": "eyJiNjQiOmZhbHNlLCJjcml0IjpbImI2NCJdLCJhbGciOiJQUzI1NiJ9..ThSJV4vVhlxYU3N7OSk6-tnKvdACfY9mhRqCVIf0eLCCSbkEyYV4sevd7AC-HGYJ2KWmMyJTm--gNogt5IuTaa5-oTegYBTyRIc_thZgxJ44_7WfpO-wAY4uyuKzt-TYVhQSWQ5lA_CpT9mL72NAGP4vnNoVvSkXhICB_g7a2Kql4xsR-wZ6htV8W4beDevhu3ajO-Q65KXQPZwInoUpWh1rcrEiyRJz9pI3146d76ikjLDe0rQSMMkm0bDQ86osncuG-HYIbwVF9xKieb6W_MupmWaZRUnvewjm1_ZQCFrKw3UCL6JeShdo7LJpM_bRkXcINEPXBWJp774yv1iyiA"
        }
    },
    "did:web:ips.dsba.aws.fiware.io:did": {
        "type": [
            "VerifiableCredential",
            "IpsActivationService"
        ],
        "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "https://w3id.org/security/suites/jws-2020/v1"
        ],
        "id": "urn:uuid:d7d35a2b-e98a-46d6-87ed-2413097dde58",
        "issuer": "did:web:marketplace.dsba.fiware.dev:did",
        "issuanceDate": "2023-08-24T14:33:08Z",
        "issued": "2023-08-24T14:33:08Z",
        "validFrom": "2023-08-24T14:33:08Z",
        "credentialSchema": {
            "id": "https://raw.githubusercontent.com/FIWARE-Ops/i4trust-provider/main/docs/schema.json",
            "type": "FullJsonSchemaValidator2021"
        },
        "credentialSubject": {
            "id": "a1d969cb-7437-4864-b94c-2b0d044c4cdc",
            "roles": [
                {
                    "names": [
                        "CREATE_ISSUER"
                    ],
                    "target": "did:web:ips.dsba.aws.fiware.io:did"
                }
            ],
            "email": "marketplace@mymail.com"
        },
        "proof": {
            "type": "JsonWebSignature2020",
            "creator": "did:web:marketplace.dsba.fiware.dev:did",
            "created": "2023-08-24T14:33:08Z",
            "verificationMethod": "did:web:marketplace.dsba.fiware.dev:did#6f4c1255f4a54090bc8ff7365b13a9b7",
            "jws": "eyJiNjQiOmZhbHNlLCJjcml0IjpbImI2NCJdLCJhbGciOiJQUzI1NiJ9..OCRyocbkjRfj6ak68bDGEYZ9cKqh8tOigQuKd-iLrC0VuZBhMAZ7YRwTw9S75NJN2dA6QvTK0ugEmL-rmNCVLNdbi-PrO0UXLhl7C0qC_rEHxvKZPrAxazKuxcrka1AQNrQzaxT36X8ocX1c-0AR5ZfjFzgIcJkqxxdaO7LQMxpp6niRf1N2s3OaS8dv9zvWBnxzvq4iEUmI70Zhzd8DgTCfxTVUVuf9f-txo4Ph5OEc2mR1ilZA6ZMMVAGfZQb463FVfqus3Nv6w5-Ot5l8f5T3p85O-miPgrQUKn3gXie57cR8ZOrBHhGqn2ule473BT1_1iU-7Er3PpVl1J5_Sg"
        }
    }
}
```
where the VCs are provided for the activation services of service providers with the DIDs 
`did:web:packetdelivery.dsba.fiware.dev:did` and `did:web:ips.dsba.aws.fiware.io:did`.
