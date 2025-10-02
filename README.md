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

### Putting it All Together — The Pipeline

The workflow of our system is structured as follows:

- **Intake**: Fetches the raw email from the inbox.
- **Parser**: Extracts structured event information from the email.
- **Calendar**: Creates the official event and invites attendees.
- **Analytics**: Logs the event for tracking and reporting purposes.
- **Reminder**: Nudges students and coordinators ahead of the event.

<img width="1475" height="587" alt="ChatGPT Image Sep 27, 2025 at 08_24_19 AM" src="https://github.com/user-attachments/assets/0a67e3a9-addd-477a-94ec-3cd64c6d6a2a" />

---

## 🚀 Setup & Configuration

### 1. Clone & Install Dependencies

```bash
git clone <repo_url>
cd "Placement Assistant"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Gmail API

Each user sets up their own Google OAuth credentials. This avoids secret sharing and ensures clean separation.

#### Step-by-step:

**Create a Google Cloud Project & Enable Gmail API**
- Go to [Google Cloud Console](https://console.cloud.google.com/) → create a project.
- Navigate to **APIs & Services** → **Library** → enable **Gmail API**.

**Create OAuth 2.0 Client ID**
- Go to **APIs & Services** → **Credentials** → **Create Credentials** → **OAuth Client ID**.
- Application type: choose **Desktop App** (or **Web App** if you have a hosted redirect).
- Download the file → `credentials.json`.

**Place Credentials**

Store it safely in your project, e.g.:
```
./credentials/credentials.json
```

Optionally export it via environment variable:
```bash
export GOOGLE_OAUTH_CLIENT_SECRETS="./credentials/credentials.json"
```

**Run OAuth Consent Flow (first-time only)**
- On first run, the script will open a browser or show a URL.
- Sign in to your Google account and grant access.
- A token will be saved locally (e.g. `./tokens/<user_email>_token.json`).
- This token will be reused until expired/revoked.

### 3. Environment Variables

Set project-specific values via `.env` or export:

```bash
export ATTENDEES="coordinator@college.edu,placement@iiit-bh.ac.in"
export EMAIL_REMINDERS_MIN="60,30"  # reminders 60 & 30 min before
export GMAIL_INCLUDE_READ=0  # 1 = include read emails, 0 = unread only
export GOOGLE_OAUTH_CLIENT_SECRETS="./credentials/credentials.json"
```

### 4. Run the Script

Example usage:

```bash
python run.py \
  --user-email user@example.com \
  --track-email "company@example.com" \
  --hours 6 \
  --max 10
```

**Parameters:**
- `--user-email` → used to store/load the correct token per user.
- `--track-email` → comma-separated list of sender emails to watch.
- `--hours` → time window to scan emails.

- `--max` → max number of emails to process.
