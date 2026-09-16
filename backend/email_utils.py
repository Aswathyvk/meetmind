import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

def send_summary_email(to_email: str, meeting_title: str, summary: str, action_items: str):
    body = f"""Hi,<br><br>
Here is the summary for the meeting: {meeting_title}<br><br>
<b>SUMMARY:</b><br>{summary}<br><br>
<b>ACTION ITEMS:</b><br>{action_items}<br><br>
— Sent automatically by MeetMind
"""

    response = requests.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {RESEND_API_KEY}"},
        json={
            "from": "MeetMind <onboarding@resend.dev>",
            "to": [to_email],
            "subject": f"Meeting Summary: {meeting_title}",
            "html": body,
        },
    )

    if response.status_code >= 400:
        raise Exception(f"Resend API error: {response.status_code} - {response.text}")