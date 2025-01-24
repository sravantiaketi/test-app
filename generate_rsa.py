import base64
import requests

# Configuration
base_url = "https://demo.docusign.net/restapi"
account_id = "YOUR_ACCOUNT_ID"
access_token = "YOUR_ACCESS_TOKEN"

# Step 1: Create Bulk List
bulk_list_url = f"{base_url}/v2.1/accounts/{account_id}/bulk_send_lists"
bulk_list_payload = {
    "name": "Bulk List Example",
    "bulkRecipients": {
        "recipients": [
            {"name": "Recipient One", "email": "recipient1@example.com", "recipientId": "1"},
            {"name": "Recipient Two", "email": "recipient2@example.com", "recipientId": "2"}
        ]
    }
}
headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
response = requests.post(bulk_list_url, json=bulk_list_payload, headers=headers)
bulk_list_id = response.json()["bulkSendListId"]

# Step 2: Create Envelope
document_content = base64.b64encode(open("document.pdf", "rb").read()).decode("utf-8")
envelope_url = f"{base_url}/v2.1/accounts/{account_id}/envelopes"
envelope_payload = {
    "emailSubject": "Please sign this document",
    "documents": [{"documentBase64": document_content, "name": "Document", "fileExtension": "pdf", "documentId": "1"}],
    "recipients": {"signers": [{"recipientId": "1", "name": "Placeholder", "email": "placeholder@example.com"}]},
    "status": "created"
}
response = requests.post(envelope_url, json=envelope_payload, headers=headers)
envelope_id = response.json()["envelopeId"]

# Step 3: Bulk Send
bulk_send_url = f"{base_url}/v2.1/accounts/{account_id}/envelopes/{envelope_id}/bulk_send"
bulk_send_payload = {"bulkSendListId": bulk_list_id}
response = requests.post(bulk_send_url, json=bulk_send_payload, headers=headers)
batch_id = response.json()["batchId"]

print(f"Bulk Send initiated. Batch ID: {batch_id}")
