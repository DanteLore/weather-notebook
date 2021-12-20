import boto3
from time import sleep


def execute_athena_command(sql):
    athena = boto3.client('athena')

    print("Executing: " + sql)

    query_start = athena.start_query_execution(
        QueryString=sql,
        QueryExecutionContext={
            'Database': "incoming"
        },
        ResultConfiguration={
            'OutputLocation': "s3://dantelore.queryresults/Unsaved/"
        }
    )

    for count in range(10):
        query_execution = athena.get_query_execution(QueryExecutionId=query_start['QueryExecutionId'])
        state = query_execution.get('QueryExecution', {}).get('Status', {}).get('State')

        if state == 'FAILED':
            print("Query failed : " + query_execution.get('QueryExecution', {}).get('Status', {}).get(
                'StateChangeReason'))
            return None
        elif state == 'SUCCEEDED':
            print('Query succeeded')
            break

        print(f"Wait count {count}/10")
        sleep(1)

    results = athena.get_query_results(QueryExecutionId=query_start['QueryExecutionId'])

    return results

