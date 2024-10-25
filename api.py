pip install fastapi uvicorn docusign-esign python-dotenv sqlalchemy
uvicorn your_script_name:app --reload


import os
import base64
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Document, Signer, SignHere, Recipients, Tabs, RecipientViewRequest
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse

# Database setup using SQLAlchemy
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# FastAPI app instance
app = FastAPI()

# DocuSign constants from environment
CLIENT_ID = os.getenv('DOCUSIGN_CLIENT_ID')
USER_ID = os.getenv('DOCUSIGN_USER_ID')
PRIVATE_KEY_PATH = os.getenv('DOCUSIGN_PRIVATE_KEY')
ACCOUNT_ID = os.getenv('DOCUSIGN_ACCOUNT_ID')
AUTH_SERVER = os.getenv('DOCUSIGN_AUTH_SERVER')
BASE_URL = 'https://demo.docusign.net/restapi'  # Use demo for sandbox

# Initialize DocuSign API Client
api_client = ApiClient(base_path=BASE_URL, o_auth_base_path=AUTH_SERVER)

# JWT Authentication function
def authenticate_with_jwt():
    try:
        with open(PRIVATE_KEY_PATH, 'r') as key_file:
            private_key = key_file.read()
        
        # Get a JWT access token
        token_response = api_client.request_jwt_user_token(
            CLIENT_ID, USER_ID, AUTH_SERVER, private_key, expires_in=3600, scopes=["signature"]
        )
        
        access_token = token_response.access_token
        api_client.set_default_header("Authorization", f"Bearer {access_token}")
        return access_token
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JWT authentication failed: {e}")

# Database setup (SQLite for demonstration, you can use PostgreSQL or MySQL)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SignerStatus(Base):
    __tablename__ = "signer_status"
    id = Column(Integer, primary_key=True, index=True)
    envelope_id = Column(String, unique=True, index=True)
    signer_email = Column(String)
    status = Column(String)  # E.g., Pending, Completed, Declined

# Create the tables
Base.metadata.create_all(bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create and send an envelope for embedded signing
def create_embedded_envelope(signer_name, signer_email, access_token):
    try:
        # Load a document to be signed (e.g., a PDF file)
        with open('document.pdf', 'rb') as file:
            doc_base64 = base64.b64encode(file.read()).decode('utf-8')
        
        # Create the document object
        document = Document(
            document_base64=doc_base64,
            name="Sample Document",
            file_extension="pdf",
            document_id="1"
        )

        # Define a signer and sign here tab
        signer = Signer(
            email=signer_email,
            name=signer_name,
            recipient_id="1",
            client_user_id="1000"  # Identifies this as an embedded signer
        )
        sign_here = SignHere(
            anchor_string="/sn1/",  # Example of an anchor string in the document
            anchor_units="pixels",
            anchor_x_offset="0",
            anchor_y_offset="0"
        )

        # Create tabs for the signer
        signer_tabs = Tabs(sign_here_tabs=[sign_here])
        signer.tabs = signer_tabs

        # Create the envelope definition
        envelope_definition = EnvelopeDefinition(
            email_subject="Please sign this document",
            documents=[document],
            recipients=Recipients(signers=[signer]),
            status="sent"  # Send the envelope immediately
        )

        # Send the envelope
        envelopes_api = EnvelopesApi(api_client)
        envelope_summary = envelopes_api.create_envelope(
            account_id=ACCOUNT_ID, envelope_definition=envelope_definition
        )
        envelope_id = envelope_summary.envelope_id
        return envelope_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create envelope: {e}")

# Generate recipient view (embedded signing URL)
def get_signing_url(envelope_id, signer_name, signer_email):
    try:
        recipient_view_request = RecipientViewRequest(
            authentication_method="none",
            client_user_id="1000",  # Matches the client_user_id of the signer
            recipient_id="1",
            return_url=f"http://127.0.0.1:8000/return?event=signing_complete&envelope_id={envelope_id}",
            user_name=signer_name,
            email=signer_email
        )

        envelopes_api = EnvelopesApi(api_client)
        recipient_view = envelopes_api.create_recipient_view(
            account_id=ACCOUNT_ID, envelope_id=envelope_id, recipient_view_request=recipient_view_request
        )
        return recipient_view.url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create recipient view: {e}")

# API route to initiate embedded signing
@app.get("/send-envelope")
def send_envelope(signer_name: str, signer_email: str, db: Session = Depends(get_db)):
    # Authenticate using JWT
    access_token = authenticate_with_jwt()

    # Create and send an envelope for the signer
    envelope_id = create_embedded_envelope(signer_name, signer_email, access_token)

    # Save the envelope ID and signer information to the database
    signer_status = SignerStatus(
        envelope_id=envelope_id,
        signer_email=signer_email,
        status="Pending"
    )
    db.add(signer_status)
    db.commit()

    # Generate the embedded signing URL
    signing_url = get_signing_url(envelope_id, signer_name, signer_email)

    # Redirect user to the embedded signing URL
    return RedirectResponse(signing_url)

# Handle the redirection after signing and update the database
@app.get("/return")
def handle_signing_return(event: str = None, envelope_id: str = None, db: Session = Depends(get_db)):
    """
    This route is the return URL where the user is redirected after completing the signing.
    You can use `event` to check if the user signed or declined and `envelope_id` to update the DB.
    """
    if event == 'signing_complete':
        # Query the signer status in the DB and update it
        signer_status = db.query(SignerStatus).filter(SignerStatus.envelope_id == envelope_id).first()
        if signer_status:
            signer_status.status = 'Completed'
            db.commit()
            return {"message": "Signing completed and database updated successfully!"}
        else:
            return {"message": "No signer found for this envelope!"}
    else:
        return {"message": f"Unhandled event: {event}"}
