import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True, parents=True)

# env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS", "credentials.json")

# gmail search query to narrow to placement mails (adjust later)
DEFAULT_GMAIL_QUERY = os.getenv(
    "GMAIL_QUERY",
    '(from:tnp OR from:placements OR subject:placement OR subject:interview) is:unread'
)

# default lookback window in hours
DEFAULT_TIME_WINDOW_HOURS = int(os.getenv("GMAIL_TIME_WINDOW_HOURS", "8"))

def build_gmail_query(track_email: str | None, hours: int | None, include_read: bool) -> str:
    """
    Build a Gmail query string including optional sender filter and time window.
    Uses Gmail's newer_than:<Nh> operator.
    """
    base = DEFAULT_GMAIL_QUERY
    # Remove unread from base; we will append based on include_read
    topic = base.replace("is:unread", "").strip()
    parts = []
    # time window
    lookback = hours if (hours and hours > 0) else DEFAULT_TIME_WINDOW_HOURS
    parts.append(f"newer_than:{lookback}h")
    if track_email:
        parts.append(f"from:{track_email}")
    # Only include the broad topic filter when no specific sender is provided
    if topic and not track_email:
        parts.append(topic)
    query = " ".join(parts).strip()
    if not include_read:
        query = f"{query} is:unread".strip()
    return query
