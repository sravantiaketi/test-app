import requests

# DocuSign API credentials
base_url = "https://demo.docusign.net/restapi"
access_token = "YOUR_ACCESS_TOKEN"
account_id = "YOUR_ACCOUNT_ID"
template_id = "YOUR_TEMPLATE_ID"
recipient_id = "YOUR_RECIPIENT_ID"

# Endpoint URL
url = f"{base_url}/v2.1/accounts/{account_id}/templates/{template_id}/recipients/{recipient_id}"

# Headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Send DELETE request
response = requests.delete(url, headers=headers)

# Check response
if response.status_code == 200:
    print("Recipient deleted successfully.")
else:
    print(f"Failed to delete recipient: {response.status_code}")
    print(response.json())
