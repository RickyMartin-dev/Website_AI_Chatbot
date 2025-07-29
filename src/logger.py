import logging

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

# import logging
# import boto3 
# from logging.handlers import RotatingFileHandler
# from datetime import datetime
# import os
# from config import S3_BUCKET

# class S3LogHandler(logging.Handler):
#     def emit(self, record):
#         log_entry = self.format(record)
#         s3 = boto3.client("s3")
#         bucket = S3_BUCKET
#         log_file = f"logs/{datetime.utcnow().isoformat()}.log"
#         s3.put_object(Bucket=bucket, Key=log_file, Body=log_entry.encode())

# def configure_logging():
#     logger = logging.getLogger("chatbot")
#     logger.setLevel(logging.INFO)

#     formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

#     # Local file logging
#     file_handler = RotatingFileHandler("chatbot.log", maxBytes=10**6, backupCount=5)
#     file_handler.setFormatter(formatter)
#     logger.addHandler(file_handler)

#     # S3 logging
#     if os.getenv("S3_BUCKET_NAME"):
#         s3_handler = S3LogHandler()
#         s3_handler.setFormatter(formatter)
#         logger.addHandler(s3_handler)
