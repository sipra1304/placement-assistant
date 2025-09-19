import asyncio
from typing import Dict, Any
from utils.parser_utils import parse_email_to_event

async def run_parser(email_dict: Dict[str, Any]) -> Dict[str, Any]:
    text = email_dict.get("body_text") or email_dict.get("snippet","")
    parsed = await parse_email_to_event(text)
    # enrich with minimal context
    parsed["email_subject"] = email_dict.get("headers",{}).get("subject","(no subject)")
    parsed["email_from"] = email_dict.get("headers",{}).get("from","")
    return parsed
