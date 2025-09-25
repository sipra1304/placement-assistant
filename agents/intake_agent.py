from typing import List, Dict, Any
import os
import re
from utils.gmail_utils import fetch_unread_emails
from utils.config import DEFAULT_GMAIL_QUERY, build_gmail_query, DEFAULT_TIME_WINDOW_HOURS

def run_intake(
    query: str | None = None,
    max_results: int = 5,
    user_email: str | None = None,
    track_email: str | None = None,
    hours: int | None = None,
    include_read: bool | None = None,
) -> List[Dict[str, Any]]:
    if include_read is None:
        include_read = os.getenv("GMAIL_INCLUDE_READ") == "1"
    if hours is None:
        hours = DEFAULT_TIME_WINDOW_HOURS
    # Build query if one is not explicitly provided
    final_query = query or build_gmail_query(track_email=track_email, hours=hours, include_read=include_read)
    return fetch_unread_emails(query=final_query, max_results=max_results, user_email=user_email)
