from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.model.event_model import EventStatus

class EventSchema(BaseModel):
    event_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: str
    max_attendees: int
    status: Optional[EventStatus] = EventStatus.scheduled

    class Config:
        orm_mode = True
