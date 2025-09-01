# Use official Python image
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY agent_service.py .
COPY agent_setup.py .
COPY remote_tools.py .
COPY agent_log.txt .
COPY envir.env .


EXPOSE 8002

CMD ["uvicorn", "agent_service:app", "--host", "0.0.0.0", "--port", "8002"]