from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSignupSchema(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class AttendeeSchema(BaseModel):
    attendee_id: Optional[int] = None
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    event_id: int

    class Config:
        orm_mode = True
