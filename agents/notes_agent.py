import google.generativeai as genai
from database.db import SessionLocal, Note
from dotenv import load_dotenv
from pathlib import Path
import os, warnings
warnings.filterwarnings("ignore")

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-lite")

def add_note(content):
    db = SessionLocal()
    try:
        note = Note(content=content)
        db.add(note)
        db.commit()
        return f"📝 Note saved: '{content}'"
    finally:
        db.close()

def get_notes():
    db = SessionLocal()
    try:
        notes = db.query(Note).all()
        if not notes:
            return "No notes found."
        result = "📝 Your notes:\n"
        for n in notes:
            result += f"- [{n.id}] {n.content}\n"
        return result
    finally:
        db.close()

def delete_note(note_id):
    db = SessionLocal()
    try:
        n = db.query(Note).filter(Note.id == note_id).first()
        if not n:
            return "Note not found."
        db.delete(n)
        db.commit()
        return f"✅ Note deleted successfully."
    finally:
        db.close()

def handle_notes_request(user_input):
    text = user_input.lower()
    if "list" in text or "show" in text:
        return get_notes()
    elif "delete" in text or "remove" in text:
        words = user_input.split()
        for word in words:
            if word.isdigit():
                return delete_note(int(word))
        return "Please mention note number to delete."
    else:
        content = user_input.replace("save note","").replace("note","").replace("save","").replace("remember","").strip()
        return add_note(content if content else user_input)