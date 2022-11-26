import boto3
from time import sleep

RESULTS_BUCKET = "dantelore.queryresults"


def execute_athena_query(sql: str, timeout: int = 30):
    athena = boto3.client('athena')

    query_start = athena.start_query_execution(
        QueryString=sql,
        QueryExecutionContext={
            'Database': "incoming"
        },
        ResultConfiguration={
            'OutputLocation': f"s3://{RESULTS_BUCKET}/Unsaved/"
        }
    )

    for count in range(timeout):
        query_execution = athena.get_query_execution(QueryExecutionId=query_start['QueryExecutionId'])
        state = query_execution.get('QueryExecution', {}).get('Status', {}).get('State')

        if state == 'FAILED':
            print("Query failed : " + query_execution.get('QueryExecution', {}).get('Status', {}).get(
                'StateChangeReason'))
            return None
        elif state == 'SUCCEEDED':
            return query_execution['QueryExecution']['ResultConfiguration']['OutputLocation']

        sleep(1)

    print(f"Query timed out after {timeout} attempts")
    return None
