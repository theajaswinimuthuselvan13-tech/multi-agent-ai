import google.generativeai as genai
from database.db import SessionLocal, Task
from dotenv import load_dotenv
from pathlib import Path
import os, warnings
warnings.filterwarnings("ignore")

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-lite")

def add_task(title):
    db = SessionLocal()
    try:
        task = Task(title=title)
        db.add(task)
        db.commit()
        return f"✅ Task added: '{title}'"
    finally:
        db.close()

def get_tasks():
    db = SessionLocal()
    try:
        tasks = db.query(Task).filter(Task.status == "pending").all()
        if not tasks:
            return "No pending tasks found."
        result = "📋 Your pending tasks:\n"
        for task in tasks:
            result += f"- [{task.id}] {task.title}\n"
        return result
    finally:
        db.close()

def complete_task(task_id):
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return "Task not found."
        task.status = "done"
        db.commit()
        return f"✅ Task '{task.title}' marked as complete!"
    finally:
        db.close()

def handle_task_request(user_input):
    text = user_input.lower()
    if "list" in text or "show" in text:
        return get_tasks()
    elif "complete" in text or "done" in text or "finish" in text:
        words = user_input.split()
        for word in words:
            if word.isdigit():
                return complete_task(int(word))
        return "Please mention task number to complete."
    else:
        title = user_input.replace("add task","").replace("add","").replace("task","").strip()
        return add_task(title if title else user_input)