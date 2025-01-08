import requests

# Replace with your actual credentials and IDs
access_token = "YOUR_ACCESS_TOKEN"
account_id = "YOUR_ACCOUNT_ID"
template_id = "YOUR_TEMPLATE_ID"

# API endpoint to fetch recipients
get_recipients_url = f"https://demo.docusign.net/restapi/v2.1/accounts/{account_id}/templates/{template_id}/recipients"

# Headers with authorization
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

# Fetch recipients
response = requests.get(get_recipients_url, headers=headers)

if response.status_code == 200:
    recipients_data = response.json()
    print("Recipients in the template:")
    for signer in recipients_data.get("signers", []):
        print(f"Name: {signer['name']}, Email: {signer['email']}, Recipient ID: {signer['recipientId']}")
else:
    print(f"Failed to fetch recipients: {response.status_code} - {response.text}")

include_anchor_tab_locations
