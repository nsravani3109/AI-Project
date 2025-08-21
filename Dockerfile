FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p data

# Set environment variables
ENV PYTHONPATH=/app
ENV DATABASE_URL=sqlite:///./data/loads.db

# Expose ports
EXPOSE 8000 8050

# Create startup script
RUN echo '#!/bin/bash\n\
python init_data.py\n\
uvicorn main:app --host 0.0.0.0 --port 8000 &\n\
python dashboard.py &\n\
wait' > start.sh && chmod +x start.sh

# Run the application
CMD ["./start.sh"]
