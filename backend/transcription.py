import os
import re
from email_utils import send_summary_email
from dotenv import load_dotenv
from faster_whisper import WhisperModel
from groq import Groq
from database import SessionLocal
import models

load_dotenv(override=True)

model = WhisperModel("base", device="cpu", compute_type="int8")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_transcript(text: str):
    prompt = f"""You are an assistant that summarizes meeting transcripts.

Transcript:
{text}

Return two sections:
1. SUMMARY: a concise paragraph summarizing the meeting.
2. ACTION_ITEMS: a list of clear action items (or "None" if none found).

Do not use markdown formatting like asterisks or bullet symbols — use plain text with hyphens for lists.
"""
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

def clean(text):
    text = text.replace("SUMMARY:", "").replace(":", "", 1)
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def transcribe_meeting(meeting_id: int, file_path: str):
    db = SessionLocal()
    try:
        meeting = db.query(models.Meeting).filter(models.Meeting.id == meeting_id).first()
        if not meeting:
            return

        meeting.status = "processing"
        db.commit()

        segments, info = model.transcribe(file_path)
        text = " ".join(segment.text.strip() for segment in segments)
        meeting.transcript = text
        db.commit()

        meeting.status = "summarizing"
        db.commit()

        result = summarize_transcript(text)

        if "ACTION_ITEMS" in result:
            summary_part, action_part = result.split("ACTION_ITEMS", 1)
        else:
            summary_part, action_part = result, "None"

        meeting.summary = clean(summary_part)
        meeting.action_items = clean(action_part)
        meeting.status = "done"
        db.commit()

        if meeting.email_to:
            try:
                send_summary_email(meeting.email_to, meeting.title, meeting.summary, meeting.action_items)
            except Exception as e:
                print(f"Email send failed: {e}")

    except Exception as e:
        meeting.status = "failed"
        meeting.transcript = (meeting.transcript or "") + f"\nError: {e}"
        db.commit()

    finally:
        db.close()