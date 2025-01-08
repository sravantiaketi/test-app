# Define the recipient details for the new recipient to be added to the existing role
new_recipient = {
    "roleName": "Signer",  # The role name that already exists in the template
    "name": "New Recipient",  # Name of the new recipient
    "email": "new_recipient@example.com",  # Optional email for the new recipient
    "routingOrder": "1",  # The order of signing (should match the existing role's order)
}

# API endpoint to update the roles of the template
update_roles_url = f"https://demo.docusign.net/restapi/v2.1/accounts/{account_id}/templates/{template_id}/roles"

# Headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

# Send the update request to modify the template roles
response = requests.put(update_roles_url, json=[new_recipient], headers=headers)

if response.status_code == 200:
    print("New recipient added to the existing role successfully!")
else:
    print(f"Failed to add recipient to role: {response.status_code} - {response.text}")
