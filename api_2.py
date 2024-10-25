import base64
from os import path
from docusign_esign import EnvelopesApi, RecipientViewRequest, Document, Signer, EnvelopeDefinition, SignHere, Tabs, Recipients
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from ...consts import authentication_method, demo_docs_path, pattern, signer_client_id
from ...docusign import create_api_client
from ...ds_config import DS_CONFIG

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class EnvelopeArgs(BaseModel):
    signer_email: str
    signer_name: str
    signer_client_id: str
    ds_return_url: str

class Args(BaseModel):
    account_id: str
    base_path: str
    access_token: str
    envelope_args: EnvelopeArgs

@app.post("/sign")
async def sign_document(request: Request, signer_email: str = Form(...), signer_name: str = Form(...)):
    envelope_args = EnvelopeArgs(
        signer_email=pattern.sub("", signer_email),
        signer_name=pattern.sub("", signer_name),
        signer_client_id=signer_client_id,
        ds_return_url=str(request.url_for("ds_return"))
    )
    args = Args(
        account_id=request.session.get("ds_account_id"),
        base_path=request.session.get("ds_base_path"),
        access_token=request.session.get("ds_access_token"),
        envelope_args=envelope_args
    )

    result = await worker(args)
    return RedirectResponse(url=result["redirect_url"])

async def worker(args: Args):
    envelope_args = args.envelope_args

    envelope_definition = make_envelope(envelope_args)

    api_client = create_api_client(base_path=args.base_path, access_token=args.access_token)
    envelope_api = EnvelopesApi(api_client)
    results = envelope_api.create_envelope(account_id=args.account_id, envelope_definition=envelope_definition)
    envelope_id = results.envelope_id

    recipient_view_request = RecipientViewRequest(
        authentication_method=authentication_method,
        client_user_id=envelope_args.signer_client_id,
        recipient_id="1",
        return_url=envelope_args.ds_return_url,
        user_name=envelope_args.signer_name,
        email=envelope_args.signer_email
    )

    results = envelope_api.create_recipient_view(
        account_id=args.account_id,
        envelope_id=envelope_id,
        recipient_view_request=recipient_view_request
    )
    return {"envelope_id": envelope_id, "redirect_url": results.url}

def make_envelope(args: EnvelopeArgs) -> EnvelopeDefinition:
    with open(path.join(demo_docs_path, DS_CONFIG["doc_pdf"]), "rb") as file:
        content_bytes = file.read()
    base64_file_content = base64.b64encode(content_bytes).decode("ascii")

    document = Document(
        document_base64=base64_file_content,
        name="Example document",
        file_extension="pdf",
        document_id="1"
    )

    signer = Signer(
        email=args.signer_email,
        name=args.signer_name,
        recipient_id="1",
        routing_order="1",
        client_user_id=args.signer_client_id
    )

    sign_here = SignHere(
        anchor_string="/sn1/",
        anchor_units="pixels",
        anchor_y_offset="10",
        anchor_x_offset="20"
    )

    signer.tabs = Tabs(sign_here_tabs=[sign_here])

    envelope_definition = EnvelopeDefinition(
        email_subject="Please sign this document sent from the Python SDK",
        documents=[document],
        recipients=Recipients(signers=[signer]),
        status="sent"
    )
    return envelope_definition
