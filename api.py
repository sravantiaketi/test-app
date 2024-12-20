import requests
import json

# Replace with your DocuSign account details
BASE_URL = "https://demo.docusign.net/restapi"  # Use production URL in live environment
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCOUNT_ID = "YOUR_ACCOUNT_ID"

# Headers for API requests
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

# Step 1: Create a Draft Envelope
def create_draft_envelope():
    url = f"{BASE_URL}/v2.1/accounts/{ACCOUNT_ID}/envelopes"
    payload = {
        "status": "created",  # Draft mode
        "emailSubject": "Please sign this document",
        "documents": [
            {
                "documentBase64": "BASE64_ENCODED_DOCUMENT_CONTENT",
                "name": "Example Document",  # Name of the document
                "fileExtension": "pdf",  # File type
                "documentId": "1",
            }
        ],
        "recipients": {
            "signers": [
                {
                    "email": "recipient@example.com",
                    "name": "Recipient Name",
                    "recipientId": "1",
                    "routingOrder": "1",
                }
            ]
        },
    }

    response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
    if response.status_code == 201:
        envelope_id = response.json()["envelopeId"]
        print(f"Draft envelope created with ID: {envelope_id}")
        return envelope_id
    else:
        print(f"Error creating draft envelope: {response.text}")
        return None

# Step 2: Generate Sender View URL
def generate_sender_view(envelope_id, return_url):
    url = f"{BASE_URL}/v2.1/accounts/{ACCOUNT_ID}/envelopes/{envelope_id}/views/sender"
    payload = {
        "returnUrl": return_url,  # URL to redirect after editing
    }

    response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
    if response.status_code == 201:
        sender_view_url = response.json()["url"]
        print(f"Sender view URL: {sender_view_url}")
        return sender_view_url
    else:
        print(f"Error generating sender view URL: {response.text}")
        return None

# Example usage
if __name__ == "__main__":
    # Replace with a valid return URL
    return_url = "https://www.example.com/return"
    
    # Step 1: Create a draft envelope
    envelope_id = create_draft_envelope()
    
    if envelope_id:
        # Step 2: Generate sender view URL
        sender_view_url = generate_sender_view(envelope_id, return_url)
        
        if sender_view_url:
            print(f"Open this URL to edit the envelope: {sender_view_url}")
