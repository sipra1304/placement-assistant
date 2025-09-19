from __future__ import annotations
import re
from datetime import datetime, timedelta
from dateutil import parser as dateparser
from typing import Optional, Dict, Any
import os

from .config import GEMINI_API_KEY

DATE_PAT = re.compile(
    r"\b(?:on\s*)?(?P<date>\d{1,2}(?:st|nd|rd|th)?[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]{3,9}\s+\d{2,4}|[A-Za-z]{3,9}\s+\d{1,2}(?:st|nd|rd|th)?,\s*\d{4})\b",
    re.IGNORECASE,
)
TIME_PAT = re.compile(
    r"\b(?:at\s*)?(?P<time>\d{1,2}(:\d{2})?\s*(?:AM|PM))\b",
    re.IGNORECASE,
)
MULTI_DAY_PAT = re.compile(
    r"\b(?P<d1>\d{1,2}(?:st|nd|rd|th)?)\s*(?:and|&|,)\s*(?P<d2>\d{1,2}(?:st|nd|rd|th)?)\s+(?P<month>[A-Za-z]{3,9})\s+(?P<year>\d{4})\b",
    re.IGNORECASE,
)
DEADLINE_WORDS = ["deadline", "last date", "submit by", "by"]

def naive_regex_extract(text: str) -> Dict[str, Any]:
    """
    Returns best-guess: {"title","start_iso","end_iso","type"}
    """
    # crude: if 'deadline' present -> set 30 min window; else 1-hour interview
    lower = text.lower()
    is_deadline = any(w in lower for w in DEADLINE_WORDS)
    title = "Placement Deadline" if is_deadline else "Placement Interview"

    # multi-day range first
    mm = MULTI_DAY_PAT.search(text)
    if mm:
        try:
            mmm = mm.groupdict()
            import re as _re
            d1 = int(_re.sub(r"[a-zA-Z]", "", mmm["d1"]))
            d2 = int(_re.sub(r"[a-zA-Z]", "", mmm["d2"]))
            month_name = mmm["month"]
            year = int(mmm["year"]) 
            start_dt = dateparser.parse(f"{d1} {month_name} {year}")
            end_dt = dateparser.parse(f"{d2} {month_name} {year}")
            start = datetime(start_dt.year, start_dt.month, start_dt.day, 10, 0)
            end = datetime(end_dt.year, end_dt.month, end_dt.day, 17, 0)
            from datetime import timezone
            import time
            offset_sec = -time.timezone if (time.localtime().tm_isdst == 0) else -time.altzone
            from datetime import timedelta as TD
            tz = timezone(TD(seconds=offset_sec))
            return {
                "title": "Placement Campus Drive",
                "start_iso": start.replace(tzinfo=tz).isoformat(),
                "end_iso": end.replace(tzinfo=tz).isoformat(),
                "type": "drive",
                "confidence": 0.8,
            }
        except Exception:
            pass

    # date
    dt = None
    m = DATE_PAT.search(text)
    if m:
        try:
            dt = dateparser.parse(m.group("date"), dayfirst=False, fuzzy=True)
        except Exception:
            dt = None

    # time
    t = None
    tm = TIME_PAT.search(text)
    if tm:
        try:
            t = dateparser.parse(tm.group("time")).time()
        except Exception:
            t = None

    if dt and t:
        start = datetime(dt.year, dt.month, dt.day, t.hour, t.minute)
    elif dt:
        # default 6pm if only date
        start = datetime(dt.year, dt.month, dt.day, 18, 0)
    else:
        # nothing found -> now+1h fallback
        start = datetime.now() + timedelta(hours=1)

    duration = timedelta(minutes=30) if is_deadline else timedelta(hours=1)
    end = start + duration

    # format with local offset (assume system local)
    from datetime import timezone
    import time
    # quick local offset
    offset_sec = -time.timezone if (time.localtime().tm_isdst == 0) else -time.altzone
    from datetime import timedelta as TD
    tz = timezone(TD(seconds=offset_sec))

    start_iso = start.replace(tzinfo=tz).isoformat()
    end_iso = end.replace(tzinfo=tz).isoformat()
    return {
        "title": title,
        "start_iso": start_iso,
        "end_iso": end_iso,
        "type": "deadline" if is_deadline else "interview",
        "confidence": 0.6 if (m or tm) else 0.3
    }

async def gemini_extract_async(text: str) -> Optional[Dict[str, Any]]:
    """
    Placeholder async call to Gemini (kept optional for Day 0).
    Returns None if GEMINI_API_KEY not set. You can fill actual call later.
    """
    if not GEMINI_API_KEY:
        return None
    # Structure we expect back
    # For now, just return None to avoid runtime dependency.
    return None

async def parse_email_to_event(text: str) -> Dict[str, Any]:
    """
    Try regex first; if low confidence and Gemini key present, try LLM fallback.
    """
    rough = naive_regex_extract(text)
    if rough["confidence"] >= 0.6:
        return rough
    llm = await gemini_extract_async(text)
    return llm or rough
