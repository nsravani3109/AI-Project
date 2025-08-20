# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port
EXPOSE 8080

# Start FastAPI with Uvicorn
CMD sh -c "python -m uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080}"