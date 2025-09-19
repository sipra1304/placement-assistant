from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os

from .config import GOOGLE_CREDENTIALS, DATA_DIR

SCOPES = ["https://www.googleapis.com/auth/calendar"]

TOKEN_PATH = DATA_DIR / "token_calendar.json"

def _auth_calendar():
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
    return build("calendar", "v3", credentials=creds)

def create_event(
    summary: str,
    start_iso: str,
    end_iso: str,
    description: str = "",
    calendar_id: str = "primary",
    attendees: Optional[List[str]] = None,
    email_reminders_minutes: Optional[List[int]] = None,
) -> str:
    """
    start_iso/end_iso must be RFC3339 with timezone, e.g. '2025-09-09T10:00:00+05:30'
    Returns event id.
    """
    if os.getenv("MOCK_MODE") == "1":
        # Return a stable fake id in mock mode
        return f"mock-event-{hash((summary, start_iso, end_iso, tuple(attendees or []), tuple(email_reminders_minutes or []))) & 0xffff}"
    service = _auth_calendar()
    event: Dict[str, Any] = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_iso},
        "end": {"dateTime": end_iso}
    }
    if attendees:
        event["attendees"] = [{"email": a} for a in attendees]
    if email_reminders_minutes is not None:
        event["reminders"] = {
            "useDefault": False,
            "overrides": [{"method": "email", "minutes": m} for m in email_reminders_minutes]
        }
    created = service.events().insert(calendarId=calendar_id, body=event).execute()
    return created.get("id")
