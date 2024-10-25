from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import os

app = FastAPI()

# DocuSign constants from environment
CLIENT_ID = os.getenv('DOCUSIGN_CLIENT_ID')
USER_ID = os.getenv('DOCUSIGN_USER_ID')
REDIRECT_URI = "https://your_redirect_url.com"  # Update this to your actual redirect URL

@app.get("/request-consent")
def request_consent():
    consent_url = (
        f"https://account-d.docusign.com/oauth/auth"
        f"?response_type=code"
        f"&scope=signature%20impersonation"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
    )
    return RedirectResponse(url=consent_url)
