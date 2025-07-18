import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
API_KEY = os.getenv("API_KEY")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://127.0.0.1:5500").split(",")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
AWS_BEDROCK_MODEL = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
DEFAULT_SYSTEM_PROMPT = "You Are a helpful assistant."