from fastapi import APIRouter, Depends
import csv
import io
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.attendee import AttendeeSchema
from app.model.attendee_model import Attendee
from app.model.event_model import Event
from app.main.config import get_db
from app.utils.auth_utils import get_current_user

router = APIRouter()

# # Register Attendee
@router.post("/register", response_model=AttendeeSchema)
def register_attendee(attendee: AttendeeSchema, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    event = db.query(Event).filter(Event.event_id == attendee.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    attendee_count = db.query(Attendee).filter(Attendee.event_id == attendee.event_id).count()
    if attendee_count >= event.max_attendees:
        raise HTTPException(status_code=400, detail="Event is full")
    existing_attendee = db.query(Attendee).filter(
        Attendee.email == attendee.email).first()
    if existing_attendee:
        # Update the existing attendee's data
        for key, value in attendee.dict(exclude_unset=True).items():
            setattr(existing_attendee, key, value)
        db.commit()
        db.refresh(existing_attendee)
        return existing_attendee
    else:
        raise HTTPException(status_code=404, detail="User not found with this email id signup first")

# List Attendees
@router.get("/list-attendees", response_model=List[AttendeeSchema])
def list_attendees(event_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return db.query(Attendee).filter(Attendee.event_id == event_id).all()


@router.post("/bulk-check-in")
async def bulk_check_in(event_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """
    Bulk check-in attendees via a CSV file.
    The CSV must have a column 'email' listing attendees' email addresses.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
    # Read CSV file
    content = await file.read()
    decoded_content = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded_content))

    if "email" not in reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV must contain an 'email' column.")
    success_count = 0
    failed_records = []
    for row in reader:
        email = row.get("email")
        if not email:
            failed_records.append({"email": None, "error": "Missing email field"})
            continue

        # Fetch attendee from DB
        attendee = db.query(Attendee).filter(
            Attendee.email == email,
            Attendee.event_id == event_id
        ).first()
        if not attendee:
            failed_records.append({"email": email, "error": "Attendee not found"})
            continue

        if attendee.check_in_status:
            failed_records.append({"email": email, "error": "Already checked in"})
            continue
        # Update check-in status
        attendee.check_in_status = True
        success_count += 1
    db.commit()  # Commit all changes
    return {
        "message": f"{success_count} attendees checked in successfully.",
        "failed_records": failed_records
    }
