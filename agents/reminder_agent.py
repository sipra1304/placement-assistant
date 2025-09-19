from utils.gmail_utils import send_email

def run_reminder(to_email: str, subject: str, body: str):
    send_email(to_email=to_email, subject=subject, body_text=body)
