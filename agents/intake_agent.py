from typing import List, Dict, Any
import os
import re
from utils.gmail_utils import fetch_unread_emails
from utils.config import DEFAULT_GMAIL_QUERY

def run_intake(query: str = DEFAULT_GMAIL_QUERY, max_results: int = 5) -> List[Dict[str, Any]]:
    if os.getenv("MOCK_MODE") == "1":
        mock_text = os.getenv(
            "MOCK_EMAIL_TEXT",
            "Interview scheduled on 25 Sep 2025 at 10:30 AM for Software Engineer."
        )
        return [{
            "id": "mock-1",
            "snippet": mock_text[:120],
            "headers": {"subject": "Mock Placement Interview", "from": "hr@example.com"},
            "body_text": mock_text,
        }]
    if os.getenv("GMAIL_INCLUDE_READ") == "1":
        query = re.sub(r"\bis:unread\b", "", query).strip()
    return fetch_unread_emails(query=query, max_results=max_results)
