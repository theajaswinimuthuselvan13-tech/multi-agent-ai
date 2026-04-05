import google.generativeai as genai
from database.db import SessionLocal, Schedule
from dotenv import load_dotenv
from pathlib import Path
import os, warnings
warnings.filterwarnings("ignore")

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-lite")

def add_schedule(event, scheduled_time):
    db = SessionLocal()
    try:
        s = Schedule(event=event, scheduled_time=scheduled_time)
        db.add(s)
        db.commit()
        return f"📅 Scheduled: '{event}' at {scheduled_time}"
    finally:
        db.close()

def get_schedule():
    db = SessionLocal()
    try:
        events = db.query(Schedule).all()
        if not events:
            return "No events scheduled."
        result = "📅 Your schedule:\n"
        for e in events:
            result += f"- [{e.id}] {e.event} at {e.scheduled_time}\n"
        return result
    finally:
        db.close()

def delete_schedule(event_id):
    db = SessionLocal()
    try:
        e = db.query(Schedule).filter(Schedule.id == event_id).first()
        if not e:
            return "Event not found."
        db.delete(e)
        db.commit()
        return f"✅ Event removed from schedule."
    finally:
        db.close()

def handle_schedule_request(user_input):
    text = user_input.lower()
    if "list" in text or "show" in text:
        return get_schedule()
    elif "delete" in text or "remove" in text:
        words = user_input.split()
        for word in words:
            if word.isdigit():
                return delete_schedule(int(word))
        return "Please mention event number to delete."
    else:
        parts = user_input.split(" at ")
        event = parts[0].replace("schedule","").replace("add","").strip()
        time = parts[1].strip() if len(parts) > 1 else "No time specified"
        return add_schedule(event, time)