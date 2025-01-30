import json
import requests

# Set your DocuSign credentials
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCOUNT_ID = "YOUR_ACCOUNT_ID"

# DocuSign API endpoint
ENVELOPE_URL = f"https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/envelopes"

# Define metadata (custom fields)
metadata_fields = [
    {"name": "ProjectID", "value": "12345"},
    {"name": "Department", "value": "Finance"}
]

# Define envelope payload
payload = {
    "emailSubject": "Envelope with Metadata",
    "documents": [
        {
            "documentId": "1",
            "name": "sample.pdf",
            "fileExtension": "pdf",
            "documentBase64": "BASE64_ENCODED_PDF"
        }
    ],
    "recipients": {
        "signers": [
            {
                "email": "recipient@example.com",
                "name": "Recipient Name",
                "recipientId": "1",
                "routingOrder": "1"
            }
        ]
    },
    "customFields": {
        "textCustomFields": metadata_fields
    },
    "status": "sent"
}

# Send request to create envelope
response = requests.post(
    ENVELOPE_URL,
    headers={"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"},
    data=json.dumps(payload),
)

if response.status_code == 201:
    envelope_id = response.json()["envelopeId"]
    print("New Envelope Created:", envelope_id)
else:
    print("Error:", response.json())
