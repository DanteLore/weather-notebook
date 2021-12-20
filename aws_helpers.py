import boto3
from time import sleep
import pandas as pd

RESULTS_BUCKET = "dantelore.queryresults"


def read_file_from_s3(url):
    print(f"Downloading data from: {url}")

    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=RESULTS_BUCKET, Key=url)

    return pd.read_csv(response.get('Body'))


def write_file_to_s3(filename, s3_bucket, s3_key):
    print("Uploading data to S3://{0}/{1}".format(s3_bucket, s3_key))

    s3 = boto3.resource('s3')
    s3.Bucket(s3_bucket).upload_file(
        filename,
        s3_key
    )


def execute_athena_query(sql: str, timeout: int = 30):
    athena = boto3.client('athena')

    print("Executing: " + sql)

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
            print('Query succeeded')
            return query_execution['QueryExecution']['ResultConfiguration']['OutputLocation']

        print(f"Wait count {count}/{timeout}")
        sleep(1)

    return None
