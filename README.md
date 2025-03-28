# Event Management API

## Overview
The Event Management API is built using **FastAPI** and provides functionality to create, manage, and track events and attendees. It supports authentication via JWT tokens and allows bulk attendee check-in through CSV uploads.

## Features
- **Event Management**: Create, update, and retrieve events
- **Attendee Management**: Register attendees, list attendees, and perform check-ins
- **Authentication**: Secure API endpoints with JWT authentication
- **Business Logic**:
  - Prevent registration if max attendees limit is reached
  - Automatically update event status based on `end_time`
  - Bulk attendee check-in via CSV upload

## Technologies Used
- **FastAPI** (Python framework)
- **SQLAlchemy** (ORM for database interactions)
- **MySQL** (Database support)
- **JWT Authentication**
- **Passlib** (For password hashing)

## Installation

### Prerequisites
- Python 3.12+
- MySQL/PostgreSQL database
- Virtual environment (optional but recommended)

### Steps to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/event-management-api.git
   cd event-management-api
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure database connection in `app/main/config.py`:
   ```python
   DATABASE_URL = "mysql+pymysql://user:password@localhost/event_management_db"
   ```
   OR for PostgreSQL:
   ```python
   DATABASE_URL = "postgresql://user:password@localhost/event_management_db"
   ```
5. Update alembic.ini
   sqlalchemy.url = mysql+pymysql://user:password@db/event_management_db

6. Run database migrations:
   ```bash
   alembic upgrade head
   ```

7. Start the server:
   ```bash
   uvicorn app.main.main:app --reload
   ```

## API Endpoints

### Authentication
- **Signup**: `POST /user_authentication/signup`
- **Login**: `POST /user_authentication/login`

### Events
- **Create Event**: `POST /events/create`
- **Update Event**: `PUT /events/edit/{event_id}`
- **List Events**: `GET /events/list-events`

### Attendees
- **Register Attendee**: `POST /attendees/register`
- **List Attendees**: `GET /attendees?event_id={event_id}`
- **Bulk Check-in (CSV Upload)**: `POST /attendees/bulk_checkin?event_id={event_id}`

## JWT Authentication
To access protected endpoints, include the JWT token in the `Authorization` header:
```bash
Authorization: Bearer <your_token_here>
```

## Testing the API
You can test the API using **Postman** or **cURL**:
```bash
curl -X POST "http://127.0.0.1:8000/events/create" -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json" -d '{ "name": "Tech Conference", "description": "An event for tech enthusiasts", "start_time": "2025-05-10T10:00:00", "end_time": "2025-05-10T18:00:00", "location": "New York", "max_attendees": 100 }'
```

## Common Issues and Fixes
- **ModuleNotFoundError: No module named 'passlib'**
  - Solution: Install dependencies using `pip install -r requirements.txt`
- **MySQL requires VARCHAR length**
  - Solution: Define `String(length=255)` for name fields in SQLAlchemy models.
- **JWT "Not authenticated" error**
  - Solution: Ensure you're passing the token in the `Authorization` header.



