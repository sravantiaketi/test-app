import requests

# Replace with your actual credentials and template details
access_token = "YOUR_ACCESS_TOKEN"
account_id = "YOUR_ACCOUNT_ID"
template_id = "YOUR_TEMPLATE_ID"

# API endpoint
url = f"https://demo.docusign.net/restapi/v2.1/accounts/{account_id}/envelopes"

# Payload to create the envelope
payload = {
    "templateId": 7a27f395-7429-48db-9e17-381fb4e53acf,
    "templateRoles": [
        {
            "email": "recipient@example.com",
            "name": "Recipient Name",
            "roleName": "Signer",  # Role name defined in the template
            "routingOrder": "1"   # Optional: Order of signing
        }
    ],
    "status": "sent"  # Use "created" to save as a draft
}

# Headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

# Send the request
response = requests.post(url, json=payload, headers=headers)

if response.status_code == 201:
    envelope_id = response.json().get("envelopeId")
    print(f"Envelope created successfully! Envelope ID: {envelope_id}")
else:
    print(f"Failed to create envelope: {response.status_code} - {response.text}")
