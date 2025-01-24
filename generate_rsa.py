import requests

# Configuration
base_url = "https://demo.docusign.net/restapi"
account_id = "YOUR_ACCOUNT_ID"
access_token = "YOUR_ACCESS_TOKEN"

# Envelope creation endpoint
url = f"{base_url}/v2.1/accounts/{account_id}/envelopes"

# Request body
request = {
    "emailSubject": "Please sign these documents",
    "status": "sent",
    "compositeTemplates": [
        {
            "serverTemplates": [
                {
                    "sequence": "1",
                    "templateId": "TEMPLATE_ID_1"
                }
            ],
            "inlineTemplates": [
                {
                    "sequence": "1",
                    "recipients": {
                        "signers": [
                            {
                                "email": "recipient1@example.com",
                                "name": "Recipient One",
                                "roleName": "Signer1"
                            }
                        ]
                    }
                }
            ]
        },
        {
            "serverTemplates": [
                {
                    "sequence": "2",
                    "templateId": "TEMPLATE_ID_2"
                }
            ],
            "inlineTemplates": [
                {
                    "sequence": "2",
                    "recipients": {
                        "signers": [
                            {
                                "email": "recipient2@example.com",
                                "name": "Recipient Two",
                                "roleName": "Signer2"
                            }
                        ]
                    }
                }
            ]
        }
    ]
}

# Headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Send the request
response = requests.post(url, json=payload, headers=headers)

# Check response
if response.status_code == 201:
    print("Envelope created successfully!")
    print("Envelope ID:", response.json().get("envelopeId"))
else:
    print(f"Failed to create envelope: {response.status_code}")
    print(response.text)
