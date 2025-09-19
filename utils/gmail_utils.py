from __future__ import annotations
import base64
import email
from email.message import EmailMessage
from typing import List, Dict, Any, Optional
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from .config import GOOGLE_CREDENTIALS, DATA_DIR

# Gmail scopes: read + send
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly",
          "https://www.googleapis.com/auth/gmail.send"]

TOKEN_PATH = DATA_DIR / "token_gmail.json"

def _auth_gmail():
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_PATH.write_text(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def fetch_unread_emails(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Returns a list of dicts: {id, snippet, payload_headers, body_text}
    """
    service = _auth_gmail()
    resp = service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
    msgs = resp.get("messages", []) or []
    out = []
    for m in msgs:
        full = service.users().messages().get(userId="me", id=m["id"], format="full").execute()
        headers = {h["name"].lower(): h["value"] for h in full["payload"].get("headers", [])}
        body_text = extract_body_text(full)
        out.append({
            "id": m["id"],
            "snippet": full.get("snippet", ""),
            "headers": headers,
            "body_text": body_text
        })
    return out

def extract_body_text(message: Dict[str, Any]) -> str:
    """
    Tries to extract 'text/plain' first; falls back to decoding 'text/html' to plain text rudimentarily.
    """
    def _walk_parts(part):
        mime = part.get("mimeType", "")
        data = part.get("body", {}).get("data")
        if data:
            raw = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
            return mime, raw
        for p in part.get("parts", []) or []:
            mime, raw = _walk_parts(p)
            if raw:
                return mime, raw
        return "", ""
    mime, raw = _walk_parts(message.get("payload", {}))
    if mime == "text/html":
        # very light HTML strip
        import re
        raw = re.sub(r"(?s)<(script|style).*?>.*?</\1>", "", raw)
        raw = re.sub(r"<br\s*/?>", "\n", raw)
        raw = re.sub(r"<.*?>", "", raw)
    return raw

def send_email(to_email: str, subject: str, body_text: str):
    service = _auth_gmail()
    msg = EmailMessage()
    msg.set_content(body_text)
    msg["To"] = to_email
    msg["From"] = "me"
    msg["Subject"] = subject

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
