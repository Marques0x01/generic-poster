import boto3
import logging as log

class DynamoService:

    dynamodb = boto3.resource('dynamodb')

    def save_item(self, objects, tableName):
        table = self.dynamodb.Table(tableName)
        posts = 0
        try:
            with table.batch_writer() as batch:
                for obj in objects:
                    posts += 1
                    batch.put_item(
                        Item=obj
                    )
        except Exception as ex:
            log.info(
                f"It was not possible to save item in table {table}: {object}. Erro: {ex}")
            raise ex
