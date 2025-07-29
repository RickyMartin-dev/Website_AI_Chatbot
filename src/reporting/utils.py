# import boto3
# import os

# LOG_GROUP_NAME = "/aws/lambda/weakly-report-of-chatapi"
# EMAIL_RECIPIENT = os.environ["REPORT_EMAIL"]
# EMAIL_SENDER = os.environ["SENDER_EMAIL"]

# def query_cloudwatch_logs(start_time, end_time):
#     logs = boto3.client("logs")

#     query = f"""
#     fields @timestamp, @message
#     | stats count(*) as total_requests,
#             count(@message like /ERROR/) as error_count,
#             count(@message like /Invalid API Key/) as unauthorized,
#             count(@message like /completed successfully/) as successes
#     """
#     response = logs.start_query(
#         logGroupName=LOG_GROUP_NAME,
#         startTime=int(start_time.timestamp()),
#         endTime=int(end_time.timestamp()),
#         queryString=query,
#     )

#     query_id = response["queryId"]

#     # Wait for query to complete (polling)
#     while True:
#         result = logs.get_query_results(queryId=query_id)
#         if result["status"] == "Complete":
#             break

#     stats = {}
#     for field in result["results"][0]:
#         stats[field["field"]] = field["value"]

#     return stats

# def send_email(html_content):
#     ses = boto3.client("ses")

#     ses.send_email(
#         Source=EMAIL_SENDER,
#         Destination={"ToAddresses": [EMAIL_RECIPIENT]},
#         Message={
#             "Subject": {"Data": "🧾 Weekly Chatbot Usage Report"},
#             "Body": {
#                 "Html": {"Data": html_content}
#             }
#         }
#     )

# def format_report(stats, start_time, end_time):
#     return f"""
#     <h2>📊 Chatbot Usage Report</h2>
#     <p><b>Date Range:</b> {start_time.date()} → {end_time.date()}</p>
#     <ul>
#         <li>Total Requests: {stats.get('total_requests', 0)}</li>
#         <li>Successful: {stats.get('successes', 0)}</li>
#         <li>Errors: {stats.get('error_count', 0)}</li>
#         <li>Unauthorized: {stats.get('unauthorized', 0)}</li>
#     </ul>
#     """