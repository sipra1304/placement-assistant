import asyncio
import argparse

from agents.intake_agent import run_intake
from agents.parser_agent import run_parser
from agents.calendar_agent import run_calendar
from agents.analytics_agent import run_analytics


async def main():
    parser = argparse.ArgumentParser(description="Placement Assistant Runner")
    parser.add_argument("--user-email", dest="user_email", default=None, help="Google account email to authenticate (stores separate token)")
    parser.add_argument("--track-email", dest="track_email", default=None, help="Filter: only emails from this sender address")
    parser.add_argument("--hours", dest="hours", type=int, default=None, help="Look back window in hours (default 8)")
    parser.add_argument("--include-read", dest="include_read", action="store_true", help="Include read emails (remove is:unread)")
    parser.add_argument("--max", dest="max_results", type=int, default=5, help="Max emails to fetch")
    args = parser.parse_args()

    emails = run_intake(
        user_email=args.user_email,
        track_email=args.track_email,
        hours=args.hours,
        include_read=args.include_read,
        max_results=args.max_results,
    )
    parsed_events = []
    for e in emails:
        parsed = await run_parser(e)
        parsed_events.append(parsed)

    created_ids = []
    for ev in parsed_events:  # create event for each parsed email
        ev_id = run_calendar(ev)
        created_ids.append(ev_id)
        run_analytics(ev, ev_id)

    return {"calendar_event_ids": created_ids}


if __name__ == "__main__":
    result = asyncio.run(main())
    from rich import print
    print("[bold green]Done.[/bold green]")
    print("Created Calendar IDs:", result.get("calendar_event_ids"))
