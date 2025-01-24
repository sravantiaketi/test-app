import requests

# Configuration
base_url = "https://demo.docusign.net/restapi"
account_id = "YOUR_ACCOUNT_ID"
envelope_id = "YOUR_ENVELOPE_ID"
access_token = "YOUR_ACCESS_TOKEN"

# Download the signed document
url = f"{base_url}/v2.1/accounts/{account_id}/envelopes/{envelope_id}/documents/combined"
headers = {"Authorization": f"Bearer {access_token}"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Save the document locally
   if response.content[:4] == b"%PDF":
        with open("signed_document.pdf", "wb") as file:
            file.write(response.content)
        print("Signed document saved successfully!")
    else:
        print("The response is not a valid PDF.")
else:
    print(f"Failed to download document: {response.status_code} - {response.text}")
