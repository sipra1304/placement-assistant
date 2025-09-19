import asyncio

from agents.intake_agent import run_intake
from agents.parser_agent import run_parser
from agents.calendar_agent import run_calendar
from agents.analytics_agent import run_analytics


async def main():
    emails = run_intake()
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
