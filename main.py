# main.py - The Reception Desk
# This is where outside world talks to our AI system

from fastapi import FastAPI
from pydantic import BaseModel
from agents.primary import primary_agent

# Create FastAPI app
app = FastAPI(
    title="Multi-Agent AI System",
    description="AI system that manages tasks, schedules and notes",
    version="1.0.0"
)

# This defines what user input looks like
class UserRequest(BaseModel):
    message: str

# Home route - just to confirm app is running
@app.get("/")
def home():
    return {
        "status": "✅ Multi-Agent AI System is Running!",
        "endpoints": [
            "/chat - Send message to AI",
            "/docs - See all endpoints"
        ]
    }

# Main chat route - this is where magic happens
@app.post("/chat")
def chat(request: UserRequest):
    """
    Send any message to the AI system.
    It will automatically route to the right agent.
    
    Examples:
    - "Add task: Complete assignment"
    - "Schedule meeting at 5pm today"
    - "Save note: Python uses indentation"
    - "Show all my tasks"
    """
    try:
        # Send to primary agent (CEO)
        response = primary_agent(request.message)
        return {
            "status": "success",
            "user_message": request.message,
            "ai_response": response
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# Health check route
@app.get("/health")
def health():
    return {"status": "healthy"}