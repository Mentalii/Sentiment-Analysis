# Use official Python image
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for transformers/torch
RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code and data
COPY rag_service.py .
COPY RAG_tool.py .
COPY student_bio.txt .

EXPOSE 8001

CMD ["uvicorn", "rag_service:app", "--host", "0.0.0.0", "--port", "8001"]