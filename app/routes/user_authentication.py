from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.attendee import UserSignupSchema, UserLoginSchema
from app.model.attendee_model import Attendee
from app.utils.auth_utils import hash_password, verify_password, create_access_token
from app.main.config import get_db
from datetime import timedelta

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserSignupSchema, db: Session = Depends(get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    existing_user = db.query(Attendee).filter(Attendee.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = hash_password(user.password)
    new_user = Attendee(email=user.email, hashed_password=hashed_pwd)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully, please login."}

@router.post("/login")
def login(user: UserLoginSchema, db: Session = Depends(get_db)):
    db_user = db.query(Attendee).filter(Attendee.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_access_token({"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}
