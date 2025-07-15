import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

def main():
    # Load .env from repo root
    load_dotenv()
    
    # Load region and bucket name from the environment (e.g. from your .env or CI secrets)
    region = os.getenv("AWS_REGION", "us-east-1")
    bucket = os.getenv("S3_BUCKET_NAME")
    if not bucket:
        raise RuntimeError("Environment variable S3_BUCKET_NAME is required")

    s3 = boto3.client("s3", region_name=region)

    # Check if the bucket exists
    try:
        s3.head_bucket(Bucket=bucket)
        print(f"Bucket exists: {bucket}")
    except ClientError as e:
        error_code = int(e.response["Error"]["Code"])
        # 404 means Not Found
        if error_code == 404:
            print(f"Bucket not found; creating: {bucket}")
            s3.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={"LocationConstraint": region}
            )
            print(f"Created bucket: {bucket}")
        else:
            # Other errors (403 Forbidden, etc.)
            raise

if __name__ == "__main__":
    main()
