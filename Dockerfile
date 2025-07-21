# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /src

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app from app.main
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]