def primary_agent(user_input):
    text = user_input.lower()
    if any(word in text for word in ["task", "todo", "add", "complete", "finish", "work"]):
        from agents.task_agent import handle_task_request
        return handle_task_request(user_input)
    elif any(word in text for word in ["schedule", "time", "event", "calendar", "meeting", "at"]):
        from agents.schedule_agent import handle_schedule_request
        return handle_schedule_request(user_input)
    elif any(word in text for word in ["note", "save", "remember", "store", "write"]):
        from agents.notes_agent import handle_notes_request
        return handle_notes_request(user_input)
    return "Please mention task, schedule, or note in your message."