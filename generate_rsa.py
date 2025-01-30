# API endpoint to get envelope custom fields
METADATA_URL = f"https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/envelopes/{envelope_id}/custom_fields"

# Send request to retrieve custom fields
response = requests.get(METADATA_URL, headers={"Authorization": f"Bearer {ACCESS_TOKEN}", "Accept": "application/json"})

if response.status_code == 200:
    custom_fields = response.json()
    print("Envelope Metadata:", custom_fields)
else:
    print("Error:", response.json())
