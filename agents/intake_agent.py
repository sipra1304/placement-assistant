from typing import List, Dict, Any
import os
import re
from utils.gmail_utils import fetch_unread_emails
from utils.config import DEFAULT_GMAIL_QUERY

def run_intake(query: str = DEFAULT_GMAIL_QUERY, max_results: int = 5) -> List[Dict[str, Any]]:
    if os.getenv("GMAIL_INCLUDE_READ") == "1":
        query = re.sub(r"\bis:unread\b", "", query).strip()
    return fetch_unread_emails(query=query, max_results=max_results)
