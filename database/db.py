# db.py - This is our filing system (SQLite Database)
# Think of this as the company's storage room

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create the database file (storage room)
engine = create_engine("sqlite:///./agent_data.db")

# Base class for all tables
Base = declarative_base()

# Table 1: Tasks
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String)          # Task name
    description = Column(String)    # Task details
    status = Column(String, default="pending")  # pending/done
    created_at = Column(DateTime, default=datetime.now)

# Table 2: Schedule
class Schedule(Base):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True)
    event = Column(String)          # Event name
    scheduled_time = Column(String) # When
    created_at = Column(DateTime, default=datetime.now)

# Table 3: Notes
class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    content = Column(String)        # Note content
    created_at = Column(DateTime, default=datetime.now)

# Create all tables in database
Base.metadata.create_all(bind=engine)

# Session = connection to database (like opening the filing cabinet)
SessionLocal = sessionmaker(bind=engine)

# Function to get database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        done