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
