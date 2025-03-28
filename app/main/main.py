from fastapi import FastAPI
from app.routes import event_routes, attendee_routes, user_authentication

app = FastAPI(title="Event Management API")

# Include the routes
app.include_router(event_routes.router, prefix="/events", tags=["Events"])
app.include_router(attendee_routes.router, prefix="/attendees", tags=["Attendees"])
app.include_router(user_authentication.router, prefix="/user_authentication", tags=["User_authentication"])

@app.get("/")
def home():
    return {"message": "Welcome to the Event Management API"}
