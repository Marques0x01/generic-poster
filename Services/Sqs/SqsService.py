import boto3
import json
import uuid
import logging as log



class SqsService:

    sqs = boto3.client('sqs')

    def write_sqs_batch(self, objects, queue):
        try:
            entries = []

            for obj in objects:
                entry = {
                    'Id': str(uuid.uuid4()),
                    'MessageBody': json.dumps(obj),
                    'DelaySeconds': 0
                }
                entries.append(entry)

            response = self.sqs.send_message_batch(QueueUrl=queue, Entries=entries)

            log.info(f"{len(response['Successful'])} messages sent. - IDs {[result['MessageId'] for result in response['Successful']]}")
        except Exception as ex:
            log.error(f"Error on sending SQS message {ex}")
            raise ex

    def get_queue_url(self, queue):
        try:
            response = self.sqs.get_queue_url(QueueName=queue)
            return response["QueueUrl"]
        except Exception as ex:
            log.error(f"Error on recovering SQS Queue {ex}")
            raise ex
