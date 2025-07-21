import json
import boto3
from src.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_BEDROCK_MODEL

from dotenv import load_dotenv
load_dotenv()

import logging
logger = logging.getLogger(__name__)

def get_bedrock_response(prompt: str, temperature=0.7, max_tokens=300) -> str:
    logger.debug("🔧 Calling Bedrock...")
    # session = boto3.session.Session(
    #     aws_access_key_id=AWS_ACCESS_KEY_ID,
    #     aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    client = boto3.client("bedrock-runtime", region_name=AWS_REGION)
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    response = client.invoke_model(
        modelId=AWS_BEDROCK_MODEL,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )
    result = json.loads(response["body"].read())
    logger.debug(f"📡 Bedrock response: {result}")
    return result["content"][0]["text"]