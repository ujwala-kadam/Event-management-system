from fastapi import FastAPI, Depends
from app.routes import event_routes, attendee_routes, user_authentication
from sqlalchemy.orm import Session
from datetime import datetime
import asyncio
from app.main.config import get_db, SessionLocal
from app.model.event_model import Event

app = FastAPI(title="Event Management API")

# Include the routes
app.include_router(event_routes.router, prefix="/events", tags=["Events"])
app.include_router(attendee_routes.router, prefix="/attendees", tags=["Attendees"])
app.include_router(user_authentication.router, prefix="/user_authentication", tags=["User_authentication"])

@app.get("/")
def home():
    return {"message": "Welcome to the Event Management API"}


async def update_event_status():
    """ Background task to update event statuses if end_time has passed. """
    while True:
        db: Session = SessionLocal()  # Create a new DB session
        try:
            now = datetime.utcnow()
            # Fetch events that have ended but not updated
            events = db.query(Event).filter(Event.end_time < now, Event.status != "completed").all()
            print(events, "eventssss")
            for event in events:
                event.status = "completed"
            db.commit()
        except Exception as e:
            print(f"Error updating event status: {e}")
        await asyncio.sleep(600)  # Run every 10 minutes


@app.on_event("startup")
async def start_background_task():
    """ Start the background task when the app starts. """
    print("Starting background task to update event statuses...")
    asyncio.create_task(update_event_status())
