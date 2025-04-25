import boto3
from datetime import datetime, timezone

# Initialize clients for the us-east-1 region
lambda_client = boto3.client('lambda', region_name='us-east-1')
logs_client = boto3.client('logs', region_name='us-east-1')

# Get list of all Lambda functions
functions = lambda_client.list_functions()['Functions']

for function in functions:
    function_name = function['FunctionName']
    log_group_name = f'/aws/lambda/{function_name}'

    try:
        # Get the latest log stream
        log_streams = logs_client.describe_log_streams(
            logGroupName=log_group_name,
            orderBy='LastEventTime',
            descending=True,
            limit=1
        )['logStreams']

        if log_streams:
            last_event_time = log_streams[0]['lastEventTimestamp']
            last_invocation_time = datetime.fromtimestamp(last_event_time / 1000, timezone.utc)
            print(f'Function: {function_name}, Last Invocation: {last_invocation_time}')
        else:
            print(f'Function: {function_name}, No invocations found')

    except logs_client.exceptions.ResourceNotFoundException:
        print(f'Function: {function_name}, Log group not found')

print("Script execution completed.")
