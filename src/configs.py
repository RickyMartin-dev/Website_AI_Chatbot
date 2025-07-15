import os
from pydantic import BaseSettings
from dotenv import load_dotenv

class Settings(BaseSettings):
    
    load_dotenv()

    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    s3_bucket: str = os.getenv("S3_BUCKET_NAME")
    api_key: str = os.getenv("API_KEY_VALUE", "CHANGE_ME")
    allowed_origin: str = os.getenv("ALLOWED_ORIGIN", "http://127.0.0.1:5500/about.html")
    bedrock_model: str = "anthropic.claude-v2"  # example will change later

    class Config:
        env_file = ".env"

config = Settings()
