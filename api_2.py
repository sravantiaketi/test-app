import requests

# Replace with your actual credentials and template details
access_token = "YOUR_ACCESS_TOKEN"
account_id = "YOUR_ACCOUNT_ID"
template_id = "YOUR_TEMPLATE_ID"

# API endpoint to fetch template details
get_template_url = f"https://demo.docusign.net/restapi/v2.1/accounts/{account_id}/templates/{template_id}"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

response = requests.get(get_template_url, headers=headers)

if response.status_code == 200:
    template_data = response.json()
    print("Template data fetched successfully!")
else:
    print(f"Failed to fetch template: {response.status_code} - {response.text}")
# Define the new recipient to add to the existing role
new_role_recipient = {
    "roleName": "Signer",  # Role already defined in the template
    "name": "New Recipient",  # Name of the new recipient
    "email": "new_recipient@example.com",  # Email of the new recipient
    "routingOrder": "1",  # The order of signing (matches existing role)
}

# Update the roles in the template data
template_data["recipients"]["signers"].append(new_role_recipient)

# API endpoint to update the template
update_template_url = f"https://demo.docusign.net/restapi/v2.1/accounts/{account_id}/templates/{template_id}"

# Send the updated template back to DocuSign
response = requests.put(update_template_url, json=template_data, headers=headers)

if response.status_code == 200:
    print("Template updated successfully with new recipient!")
else:
    print(f"Failed to update template: {response.status_code} - {response.text}")
