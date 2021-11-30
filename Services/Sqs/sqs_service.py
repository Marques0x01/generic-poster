import boto3, json

sqs = boto3.client('sqs')

def send_sqs(obj, queue):
    response = sqs.send_message(
        QueueUrl=get_queue_url(queue),
        DelaySeconds=10,
        MessageBody=str(obj)
    )

    return response['MessageId']

def get_queue_url(queue):
    response = sqs.get_queue_url(
        QueueName=queue,
    )
    return response["QueueUrl"]