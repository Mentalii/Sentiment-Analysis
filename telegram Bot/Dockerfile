# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code
COPY telegram_bot.py .

# Expose any necessary ports (not needed for Telegram bot, but included for completeness)
EXPOSE 8003

# Run the bot
CMD ["python", "telegram_bot.py"]

