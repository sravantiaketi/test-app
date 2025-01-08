import requests

# Replace with your actual credentials and IDs
access_token = "YOUR_ACCESS_TOKEN"
account_id = "YOUR_ACCOUNT_ID"
envelope_id = "YOUR_ENVELOPE_ID"

# Step 1: Get the list of documents in the envelope
list_url = f"https://demo.docusign.net/restapi/v2.1/accounts/{account_id}/envelopes/{envelope_id}/documents"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/json",
}

list_response = requests.get(list_url, headers=headers)

if list_response.status_code == 200:
    documents = list_response.json().get("envelopeDocuments", [])
    print("Documents in the envelope:")
    for doc in documents:
        print(f"Document ID: {doc['documentId']}, Name: {doc['name']}")

    # Step 2: Download the first document (example)
    if documents:
        document_id = documents[0]['documentId']  # Example: first document
        document_name = documents[0]['name']

        download_url = f"{list_url}/{document_id}"
        download_response = requests.get(download_url, headers=headers)

        if download_response.status_code == 200:
            # Save the document locally
            with open(document_name, "wb") as file:
                file.write(download_response.content)
            print(f"Document '{document_name}' downloaded successfully.")
        else:
            print(f"Failed to download document: {download_response.status_code} - {download_response.text}")
    else:
        print("No documents found in the envelope.")
else:
    print(f"Failed to fetch document list: {list_response.status_code} - {list_response.text}")
