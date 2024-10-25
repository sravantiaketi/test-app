from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import os
from fastapi import FastAPI, Request
import os

app = FastAPI()

CLIENT_ID = os.getenv('DOCUSIGN_CLIENT_ID')
USER_ID = os.getenv('DOCUSIGN_USER_ID')
REDIRECT_URI = "http://localhost:8000/docusign-callback"  # Make sure this matches your DocuSign app's redirect URI

@app.get("/docusign-callback")
async def docusign_callback(request: Request):
    # Capture the query parameters returned by DocuSign (e.g., authorization code)
    query_params = request.query_params
    auth_code = query_params.get("code")
    
    # Log the auth code for debugging
    if auth_code:
        print(f"Authorization code received: {auth_code}")
    else:
        print("No authorization code received. Check if consent was granted.")

    # Inform user of successful redirection
    return {"message": "Successfully redirected from DocuSign!", "authorization_code": auth_code}


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
