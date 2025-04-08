# Use official Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependencies file and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app
COPY . .

# Expose port
EXPOSE 8000

# Start the app
CMD ["uvicorn", "app.main.main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD alembic upgrade head && uvicorn app.main.main:app --host 0.0.0.0 --port 8000
