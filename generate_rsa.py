import requests

# DocuSign API credentials
base_url = "https://demo.docusign.net/restapi"
access_token = "YOUR_ACCESS_TOKEN"
account_id = "YOUR_ACCOUNT_ID"
template_id = "YOUR_TEMPLATE_ID"

# New signers to replace existing ones
new_signers = {
    "recipients": {
        "signers": [
            {
                "recipientId": "1",
                "email": "new.signer1@example.com",
                "name": "New Signer One",
                "roleName": "Signer"
            },
            {
                "recipientId": "2",
                "email": "new.signer2@example.com",
                "name": "New Signer Two",
                "roleName": "Signer"
            }
        ]
    }
}

# Update recipients in the template
url = f"{base_url}/v2.1/accounts/{account_id}/templates/{template_id}/recipients"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
response = requests.put(url, headers=headers, json=new_signers)

# Check the response
if response.status_code == 200:
    print("Recipients updated successfully.")
else:
    print(f"Failed to update recipients: {response.status_code}")
    print(response.json())
