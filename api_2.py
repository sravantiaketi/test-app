# API endpoint to get template recipient tabs
get_tabs_url = f"https://demo.docusign.net/restapi/v2.1/accounts/{account_id}/templates/{template_id}/recipients/tabs"

response = requests.get(get_tabs_url, headers=headers)

if response.status_code == 200:
    tabs_data = response.json()
    print("Tabs data for the template:", tabs_data)
else:
    print(f"Failed to fetch tabs: {response.status_code} - {response.text}")

If the signHereTabs or other tabs are not showing for a new recipient added to a role in a DocuSign template, it's likely due to how tabs are associated with roles in the template. Tabs are not automatically inherited by new recipients unless explicitly defined or mapped correctly.

Here’s how you can address this issue:

Root Cause
Tabs Are Role-Specific: Tabs in DocuSign templates are associated with specific roles, not recipients. When you add a new recipient to a role, the tabs must either:
Be explicitly assigned to the recipient, or
Be inherited from the role if the role is reused properly.
Recipient-Specific Tab Assignment: If the tabs are not showing, the new recipient might not be properly linked to the role's tabs.
Solution: Explicitly Assign Tabs to the New Recipient
You can explicitly assign the existing tabs to the new recipient by fetching the tabs from the role and reapplying them.

Step 1: Fetch Tabs Associated with the Role
Retrieve the tabs associated with the role from the template.

python
Copy code
# API endpoint to get template recipient tabs
get_tabs_url = f"https://demo.docusign.net/restapi/v2.1/accounts/{account_id}/templates/{template_id}/recipients/tabs"

response = requests.get(get_tabs_url, headers=headers)

if response.status_code == 200:
    tabs_data = response.json()
    print("Tabs data for the template:", tabs_data)
else:
    print(f"Failed to fetch tabs: {response.status_code} - {response.text}")
Step 2: Add Recipient with Tabs
Use the retrieved tabs to assign them to the new recipient. Ensure the recipientId matches the ID of the new recipient you are adding.

python
Copy code
# Define the new recipient with the tabs
new_recipient_with_tabs = {
    "roleName": "Signer",  # Role already defined in the template
    "name": "New Recipient",
    "email": "new_recipient@example.com",
    "routingOrder": "1",
    "recipientId": "2",  # Unique ID for the new recipient
    "tabs": tabs_data  # Assign the fetched tabs to the new recipient
}
