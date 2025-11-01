# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /bot

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot source code
COPY . .

# Run the bot
CMD ["python3", "-m", "bot.bot"]
