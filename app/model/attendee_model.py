from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.main.config import Base

class Attendee(Base):
    __tablename__ = "attendees"

    attendee_id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=True)
    event_id = Column(Integer, ForeignKey("events.event_id"), nullable=True)
    check_in_status = Column(Boolean, default=False)
