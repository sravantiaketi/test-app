import requests

# Set variables
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCOUNT_ID = "YOUR_ACCOUNT_ID"
ENVELOPE_ID = "YOUR_ENVELOPE_ID"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json"
}

# Get document list from envelope
url = f"https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/envelopes/{ENVELOPE_ID}/documents"
response = requests.get(url, headers=HEADERS)

if response.status_code == 200:
    documents = response.json().get("documents", [])
    print("Documents in Envelope:", documents)
else:
    print("Error:", response.json())





import os

DOWNLOAD_PATH = "documents"

# Ensure directory exists
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Loop through documents
for doc in documents:
    doc_id = doc["documentId"]
    doc_name = doc["name"]

    # Get document content
    doc_url = f"https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/envelopes/{ENVELOPE_ID}/documents/{doc_id}"
    doc_response = requests.get(doc_url, headers=HEADERS)

    if doc_response.status_code == 200:
        file_path = os.path.join(DOWNLOAD_PATH, doc_name)
        with open(file_path, "wb") as file:
            file.write(doc_response.content)
        print(f"Downloaded: {doc_name}")
    else:
        print(f"Failed to fetch {doc_name}")




import json

# New envelope details
NEW_ENVELOPE_URL = f"https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/envelopes"

# Define documents for new envelope
document_objects = []
for doc in documents:
    doc_id = doc["documentId"]
    doc_name = doc["name"]

    with open(os.path.join(DOWNLOAD_PATH, doc_name), "rb") as file:
        encoded_content = base64.b64encode(file.read()).decode()

    document_objects.append({
        "documentId": doc_id,
        "name": doc_name,
        "fileExtension": "pdf",
        "documentBase64": encoded_content
    })

# Define envelope payload
payload = {
    "emailSubject": "New Envelope from Existing Documents",
    "documents": document_objects,
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
    "status": "sent"
}

# Send request to create new envelope
create_response = requests.post(NEW_ENVELOPE_URL, headers={**HEADERS, "Content-Type": "application/json"}, data=json.dumps(payload))

if create_response.status_code == 201:
    print("New Envelope Created:", create_response.json()["envelopeId"])
else:
    print("Error:", create_response.json())
