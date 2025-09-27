# Placement Assistant – Multi-Agent System

Automatically fetch placement emails, extract deadlines/interviews, create Google Calendar events, and log analytics. Optional reminders.

---

## Features
- Gmail intake with customizable query filters
- Date/time parsing (deadlines, interviews, multi-day events)
- Google Calendar event creation with attendees & reminders
- Analytics logging (`data/analytics_log.csv`)

---

## Prerequisites
- Python 3.10+
- Google OAuth credentials JSON (`credentials.json`) in project root

---
## Workflow
<img width="1475" height="587" alt="ChatGPT Image Sep 27, 2025 at 08_24_19 AM" src="https://github.com/user-attachments/assets/0a67e3a9-addd-477a-94ec-3cd64c6d6a2a" />


---


## Setup
```bash!

cd "Placement Assistant"
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
