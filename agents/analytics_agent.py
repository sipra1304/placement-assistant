import csv
from pathlib import Path
from typing import Dict, Any
from utils.config import DATA_DIR

LOG_PATH = DATA_DIR / "analytics_log.csv"

def run_analytics(event_payload: Dict[str, Any], calendar_event_id: str):
    exists = LOG_PATH.exists()
    with LOG_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "email_from","email_subject","type","start_iso","end_iso","calendar_event_id","confidence"
            ]
        )
        if not exists:
            writer.writeheader()
        writer.writerow({
            "email_from": event_payload.get("email_from",""),
            "email_subject": event_payload.get("email_subject",""),
            "type": event_payload.get("type","event"),
            "start_iso": event_payload.get("start_iso",""),
            "end_iso": event_payload.get("end_iso",""),
            "calendar_event_id": calendar_event_id,
            "confidence": event_payload.get("confidence",0.0)
        })
