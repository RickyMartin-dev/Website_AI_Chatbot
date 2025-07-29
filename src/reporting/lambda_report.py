# import boto3
# import logging
# from datetime import datetime, timedelta
# from utils import (
#     query_cloudwatch_logs,
#     format_report,
#     send_email
# )

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

# def lambda_handler(event, context):
#     # Calculate the time range (last 7 days)
#     end_time = datetime.utcnow()
#     start_time = end_time - timedelta(days=7)

#     # Fetch log metrics from CloudWatch
#     stats = query_cloudwatch_logs(start_time, end_time)

#     # Format summary text
#     html_body = format_report(stats, start_time, end_time)

#     # Send report email
#     send_email(html_body)
    
#     return {
#         "statusCode": 200,
#         "body": "Report sent."
#     }
