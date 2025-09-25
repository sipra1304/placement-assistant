from typing import Dict, List, Optional
import os
from utils.calendar_utils import create_event

def run_calendar(event_payload: Dict) -> str:
    title = event_payload.get("title","Placement Event")
    start_iso = event_payload["start_iso"]
    end_iso = event_payload["end_iso"]
    desc = f"{event_payload.get('type','event').title()} from email: {event_payload.get('email_subject','')}"
    attendees_env = os.getenv("ATTENDEES", "").strip()
    attendees: Optional[List[str]] = [a.strip() for a in attendees_env.split(",") if a.strip()] if attendees_env else None
    reminders_env = os.getenv("EMAIL_REMINDERS_MIN", "").strip()
    if reminders_env:
        email_reminders_minutes: Optional[List[int]] = [int(x) for x in reminders_env.split(",") if x.strip().isdigit()]
    else:
        # default reminders at 60 and 30 minutes before the event
        email_reminders_minutes = [60, 30]
    return create_event(title, start_iso, end_iso, desc, attendees=attendees, email_reminders_minutes=email_reminders_minutes)
