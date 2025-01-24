import requests

def download_signed_envelope_as_pdf(account_id, envelope_id, access_token, output_file):
    """
    Downloads the signed envelope as a combined PDF file.

    Args:
        account_id (str): Your DocuSign account ID.
        envelope_id (str): The ID of the envelope.
        access_token (str): Your DocuSign OAuth access token.
        output_file (str): The path and filename to save the downloaded PDF.

    Returns:
        None
    """

    url = f"https://{region}.docusign.com/restapi/v2.1/accounts/{account_id}/envelopes/{envelope_id}/documents/combined"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/pdf"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes

        with open(output_file, "wb") as f:
            f.write(response.content)

        print(f"Signed envelope downloaded successfully to: {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading envelope: {e}")

# Usage:
account_id = "your_account_id"
envelope_id = "your_envelope_id"
access_token = "your_access_token"
output_file = "signed_envelope.pdf" 

download_signed_envelope_as_pdf(account_id, envelope_id, access_token, output_file)
