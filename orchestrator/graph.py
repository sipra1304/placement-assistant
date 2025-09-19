from typing import List, Dict, Any
from langgraph.graph import StateGraph, END

# agents
from agents.intake_agent import run_intake
from agents.parser_agent import run_parser
from agents.calendar_agent import run_calendar
from agents.analytics_agent import run_analytics

# simple state type
class State(dict):
    pass

def node_intake(state: State) -> State:
    emails = run_intake()
    state["emails"] = emails
    return state

async def node_parse(state: State) -> State:
    emails: List[Dict[str,Any]] = state.get("emails",[])
    parsed_events = []
    for e in emails:
        parsed = await run_parser(e)
        parsed_events.append(parsed)
    state["parsed_events"] = parsed_events
    return state

def node_calendar(state: State) -> State:
    # create events for top 1 (Day 0 demo)
    events = state.get("parsed_events",[])
    created_ids = []
    for ev in events[:1]:
        ev_id = run_calendar(ev)
        created_ids.append(ev_id)
        # log analytics
        run_analytics(ev, ev_id)
    state["calendar_event_ids"] = created_ids
    return state

def build_graph():
    g = StateGraph(State)
    g.add_node("intake", node_intake)
    g.add_node("parse", node_parse)
    g.add_node("calendar", node_calendar)

    g.set_entry_point("intake")
    g.add_edge("intake", "parse")
    g.add_edge("parse", "calendar")
    g.add_edge("calendar", END)
    return g.compile()
