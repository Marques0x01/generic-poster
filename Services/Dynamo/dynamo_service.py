import boto3

dynamodb = boto3.resource('dynamodb')


def save_item(objects, tableName):
    table = dynamodb.Table(tableName)
    posts = 0
    try:
        with table.batch_writer() as batch:
            for obj in objects:
                posts += 1
                batch.put_item(
                    Item=obj
                )
                print(f"Posted: {posts}")
    except:
        print(f"It was not possible to save item in table {table}: {object}")
        raise