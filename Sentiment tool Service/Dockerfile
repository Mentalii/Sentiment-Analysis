FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for transformers/torch
RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir torch transformers
RUN pip install --no-cache-dir -r requirements.txt

# Copy your service code
COPY sentiment_service.py .

# Expose port for FastAPI
EXPOSE 8000

# Start the service
CMD ["uvicorn", "sentiment_service:app", "--host", "0.0.0.0", "--port", "8000"]