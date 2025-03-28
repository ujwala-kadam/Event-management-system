from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app.schemas.event import EventSchema
from app.model.event_model import Event
from app.main.config import get_db
from datetime import datetime, timedelta
from typing import List
from app.utils.auth_utils import get_current_user

router = APIRouter()


@router.post("/create", response_model=EventSchema)
def create_event(event: EventSchema, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Check if an event with the same name already exists
    existing_event = db.query(Event).filter(Event.name == event.name).first()
    if existing_event:
        raise HTTPException(status_code=400, detail="Event with this name already exists")
    new_event = Event(**event.dict())
    new_event.status = "scheduled"  # Default status
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

# Update Event
@router.put("/edit/{event_id}", response_model=EventSchema)
def update_event(event_id: int, event_update: EventSchema, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    for key, value in event_update.dict(exclude_unset=True).items():
        setattr(event, key, value)
    db.commit()
    db.refresh(event)
    return event


#list events
@router.get("/list-events", response_model=List[EventSchema])
def list_events(status: str = None, location: str = None, date: datetime = None, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    query = db.query(Event)
    if status:
        query = query.filter(Event.status == status)
    if location:
        query = query.filter(Event.location == location)
    if date:
        query = query.filter(Event.start_time >= date, Event.end_time <= date + timedelta(days=1))
    result =  query.all()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Event not found for given category")

