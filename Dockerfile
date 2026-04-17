FROM python:3.11-slim

# Install system dependencies including Rust for pydantic-core
RUN apt-get update && apt-get install -y gcc cargo rustc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the application
COPY . .

# Command to run the bot
CMD ["python", "bot.py"]