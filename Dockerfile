# Use official Python image
# FROM python:3.11-slim
# FROM public.ecr.aws/lambda/python:3.11
# FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.11
FROM public.ecr.aws/lambda/python:3.11

# Set working directory
# WORKDIR /src

# Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# COPY requirements.txt .
COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install -r requirements.txt

# Copy the source code
# COPY src/ ./src
COPY src/ ${LAMBDA_TASK_ROOT}/src/

# Expose FastAPI port
# EXPOSE 8000

# Run FastAPI app from src.main
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["src.main.handler"]