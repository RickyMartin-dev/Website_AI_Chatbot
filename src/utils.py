import boto3
import os
import json
from datetime import datetime

s3 = boto3.client("s3")
S3_BUCKET = os.getenv("LOG_BUCKET")

def log_to_s3(input_text, output_text):
    if not S3_BUCKET:
        return
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "input": input_text,
        "output": output_text
    }
    filename = f"logs/{datetime.utcnow().isoformat()}.json"
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=filename,
        Body=json.dumps(log_data),
        ContentType="application/json"
    )
