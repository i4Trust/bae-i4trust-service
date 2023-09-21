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
and needs to be configured in the BAE charging backend with the ENV `BAE_PLUGIN_VC`.

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

This translates to the ENV:
```shell
BAE_PLUGIN_VC=ewogICAgImRpZDp3ZWI6cGFja2V0ZGVsaXZlcnkuZHNiYS5maXdhcmUuZGV2OmRpZCI6IHsKICAgICAgICAidHlwZSI6IFsKICAgICAgICAgICAgIlZlcmlmaWFibGVDcmVkZW50aWFsIiwKICAgICAgICAgICAgIkFjdGl2YXRpb25TZXJ2aWNlIgogICAgICAgIF0sCiAgICAgICAgIkBjb250ZXh0IjogWwogICAgICAgICAgICAiaHR0cHM6Ly93d3cudzMub3JnLzIwMTgvY3JlZGVudGlhbHMvdjEiLAogICAgICAgICAgICAiaHR0cHM6Ly93M2lkLm9yZy9zZWN1cml0eS9zdWl0ZXMvandzLTIwMjAvdjEiCiAgICAgICAgXSwKICAgICAgICAiaWQiOiAidXJuOnV1aWQ6YzdlN2Q0YTEtNzU3OS00MGEzLWI0MTgtNTlmNmE5ZjJmNmIxIiwKICAgICAgICAiaXNzdWVyIjogImRpZDp3ZWI6bWFya2V0cGxhY2UuZHNiYS5maXdhcmUuZGV2OmRpZCIsCiAgICAgICAgImlzc3VhbmNlRGF0ZSI6ICIyMDIzLTA2LTA3VDA3OjQ1OjA2WiIsCiAgICAgICAgImlzc3VlZCI6ICIyMDIzLTA2LTA3VDA3OjQ1OjA2WiIsCiAgICAgICAgInZhbGlkRnJvbSI6ICIyMDIzLTA2LTA3VDA3OjQ1OjA2WiIsCiAgICAgICAgImV4cGlyYXRpb25EYXRlIjogIjIwMzItMTItMDhUMTM6MDU6MDZaIiwKICAgICAgICAiY3JlZGVudGlhbFNjaGVtYSI6IHsKICAgICAgICAgICAgImlkIjogImh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9GSVdBUkUtT3BzL2k0dHJ1c3QtcHJvdmlkZXIvbWFpbi9kb2NzL3NjaGVtYS5qc29uIiwKICAgICAgICAgICAgInR5cGUiOiAiRnVsbEpzb25TY2hlbWFWYWxpZGF0b3IyMDIxIgogICAgICAgIH0sCiAgICAgICAgImNyZWRlbnRpYWxTdWJqZWN0IjogewogICAgICAgICAgICAiaWQiOiAiMGI4NzYwMDAtMzZjNy00N2VkLWI4OTYtNWI1ZWMxNjM2NjNhIiwKICAgICAgICAgICAgInJvbGVzIjogWwogICAgICAgICAgICAgICAgewogICAgICAgICAgICAgICAgICAgICJuYW1lcyI6IFsKICAgICAgICAgICAgICAgICAgICAgICAgIkNSRUFURV9JU1NVRVIiCiAgICAgICAgICAgICAgICAgICAgXSwKICAgICAgICAgICAgICAgICAgICAidGFyZ2V0IjogImRpZDp3ZWI6cGFja2V0ZGVsaXZlcnkuZHNiYS5maXdhcmUuZGV2OmRpZCIKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgXSwKICAgICAgICAgICAgImVtYWlsIjogIm1hcmtldHBsYWNlQG15bWFpbC5jb20iCiAgICAgICAgfSwKICAgICAgICAicHJvb2YiOiB7CiAgICAgICAgICAgICJ0eXBlIjogIkpzb25XZWJTaWduYXR1cmUyMDIwIiwKICAgICAgICAgICAgImNyZWF0b3IiOiAiZGlkOndlYjptYXJrZXRwbGFjZS5kc2JhLmZpd2FyZS5kZXY6ZGlkIiwKICAgICAgICAgICAgImNyZWF0ZWQiOiAiMjAyMy0wNi0wN1QwNzo0NTowNloiLAogICAgICAgICAgICAidmVyaWZpY2F0aW9uTWV0aG9kIjogImRpZDp3ZWI6bWFya2V0cGxhY2UuZHNiYS5maXdhcmUuZGV2OmRpZCM2ZjRjMTI1NWY0YTU0MDkwYmM4ZmY3MzY1YjEzYTliNyIsCiAgICAgICAgICAgICJqd3MiOiAiZXlKaU5qUWlPbVpoYkhObExDSmpjbWwwSWpwYkltSTJOQ0pkTENKaGJHY2lPaUpRVXpJMU5pSjkuLlRoU0pWNHZWaGx4WVUzTjdPU2s2LXRuS3ZkQUNmWTltaFJxQ1ZJZjBlTENDU2JrRXlZVjRzZXZkN0FDLUhHWUoyS1dtTXlKVG0tLWdOb2d0NUl1VGFhNS1vVGVnWUJUeVJJY190aFpneEo0NF83V2ZwTy13QVk0dXl1S3p0LVRZVmhRU1dRNWxBX0NwVDltTDcyTkFHUDR2bk5vVnZTa1hoSUNCX2c3YTJLcWw0eHNSLXdaNmh0VjhXNGJlRGV2aHUzYWpPLVE2NUtYUVBad0lub1VwV2gxcmNyRWl5Ukp6OXBJMzE0NmQ3NmlrakxEZTByUVNNTWttMGJEUTg2b3NuY3VHLUhZSWJ3VkY5eEtpZWI2V19NdXBtV2FaUlVudmV3am0xX1pRQ0ZyS3czVUNMNkplU2hkbzdMSnBNX2JSa1hjSU5FUFhCV0pwNzc0eXYxaXlpQSIKICAgICAgICB9CiAgICB9LAogICAgImRpZDp3ZWI6aXBzLmRzYmEuYXdzLmZpd2FyZS5pbzpkaWQiOiB7CiAgICAgICAgInR5cGUiOiBbCiAgICAgICAgICAgICJWZXJpZmlhYmxlQ3JlZGVudGlhbCIsCiAgICAgICAgICAgICJJcHNBY3RpdmF0aW9uU2VydmljZSIKICAgICAgICBdLAogICAgICAgICJAY29udGV4dCI6IFsKICAgICAgICAgICAgImh0dHBzOi8vd3d3LnczLm9yZy8yMDE4L2NyZWRlbnRpYWxzL3YxIiwKICAgICAgICAgICAgImh0dHBzOi8vdzNpZC5vcmcvc2VjdXJpdHkvc3VpdGVzL2p3cy0yMDIwL3YxIgogICAgICAgIF0sCiAgICAgICAgImlkIjogInVybjp1dWlkOmQ3ZDM1YTJiLWU5OGEtNDZkNi04N2VkLTI0MTMwOTdkZGU1OCIsCiAgICAgICAgImlzc3VlciI6ICJkaWQ6d2ViOm1hcmtldHBsYWNlLmRzYmEuZml3YXJlLmRldjpkaWQiLAogICAgICAgICJpc3N1YW5jZURhdGUiOiAiMjAyMy0wOC0yNFQxNDozMzowOFoiLAogICAgICAgICJpc3N1ZWQiOiAiMjAyMy0wOC0yNFQxNDozMzowOFoiLAogICAgICAgICJ2YWxpZEZyb20iOiAiMjAyMy0wOC0yNFQxNDozMzowOFoiLAogICAgICAgICJjcmVkZW50aWFsU2NoZW1hIjogewogICAgICAgICAgICAiaWQiOiAiaHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0ZJV0FSRS1PcHMvaTR0cnVzdC1wcm92aWRlci9tYWluL2RvY3Mvc2NoZW1hLmpzb24iLAogICAgICAgICAgICAidHlwZSI6ICJGdWxsSnNvblNjaGVtYVZhbGlkYXRvcjIwMjEiCiAgICAgICAgfSwKICAgICAgICAiY3JlZGVudGlhbFN1YmplY3QiOiB7CiAgICAgICAgICAgICJpZCI6ICJhMWQ5NjljYi03NDM3LTQ4NjQtYjk0Yy0yYjBkMDQ0YzRjZGMiLAogICAgICAgICAgICAicm9sZXMiOiBbCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgIm5hbWVzIjogWwogICAgICAgICAgICAgICAgICAgICAgICAiQ1JFQVRFX0lTU1VFUiIKICAgICAgICAgICAgICAgICAgICBdLAogICAgICAgICAgICAgICAgICAgICJ0YXJnZXQiOiAiZGlkOndlYjppcHMuZHNiYS5hd3MuZml3YXJlLmlvOmRpZCIKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgXSwKICAgICAgICAgICAgImVtYWlsIjogIm1hcmtldHBsYWNlQG15bWFpbC5jb20iCiAgICAgICAgfSwKICAgICAgICAicHJvb2YiOiB7CiAgICAgICAgICAgICJ0eXBlIjogIkpzb25XZWJTaWduYXR1cmUyMDIwIiwKICAgICAgICAgICAgImNyZWF0b3IiOiAiZGlkOndlYjptYXJrZXRwbGFjZS5kc2JhLmZpd2FyZS5kZXY6ZGlkIiwKICAgICAgICAgICAgImNyZWF0ZWQiOiAiMjAyMy0wOC0yNFQxNDozMzowOFoiLAogICAgICAgICAgICAidmVyaWZpY2F0aW9uTWV0aG9kIjogImRpZDp3ZWI6bWFya2V0cGxhY2UuZHNiYS5maXdhcmUuZGV2OmRpZCM2ZjRjMTI1NWY0YTU0MDkwYmM4ZmY3MzY1YjEzYTliNyIsCiAgICAgICAgICAgICJqd3MiOiAiZXlKaU5qUWlPbVpoYkhObExDSmpjbWwwSWpwYkltSTJOQ0pkTENKaGJHY2lPaUpRVXpJMU5pSjkuLk9DUnlvY2JralJmajZhazY4YkRHRVlaOWNLcWg4dE9pZ1F1S2QtaUxyQzBWdVpCaE1BWjdZUndUdzlTNzVOSk4yZEE2UXZUSzB1Z0VtTC1ybU5DVkxOZGJpLVByTzBVWExobDdDMHFDX3JFSHh2S1pQckF4YXpLdXhjcmthMUFRTnJRemF4VDM2WDhvY1gxYy0wQVI1WmZqRnpnSWNKa3F4eGRhTzdMUU14cHA2bmlSZjFOMnMzT2FTOGR2OXp2V0JueHp2cTRpRVVtSTcwWmh6ZDhEZ1RDZnhUVlVWdWY5Zi10eG80UGg1T0VjMm1SMWlsWkE2Wk1NVkFHZlpRYjQ2M0ZWZnF1czNOdjZ3NS1PdDVsOGY1VDNwODVPLW1pUGdyUVVLbjNnWGllNTdjUjhaT3JCSGhHcW4ydWxlNDczQlQxXzFpVS03RXIzUHBWbDFKNV9TZyIKICAgICAgICB9CiAgICB9Cn0=
```
