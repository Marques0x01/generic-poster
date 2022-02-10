from mimetypes import init
from flask import Flask, request
from Services.Process.OrchestratorService import OrchestratorService
from Services.Process.ValidationService import ValidationService
from Services.Dynamo.DynamoService import DynamoService
from Services.Sqs.SqsService import SqsService
import logging as log
from Configurantion.LoggingConfiguration import init_logs
from Services.Kafka.KafkaService import KafkaService

app = Flask(__name__)


@app.route("/dynamo", methods=['POST'])
def save_dynamo():
    try:
        log.info(f"Starting process...")

        json_dict = request.get_json()
        loops = json_dict["amount"]
        ValidationService.check_type(loops, "int")

        objects = []

        log.info("Processing data...")

        for _ in range(loops):
            obj = OrchestratorService().process_dict(json_dict["data"])
            objects.append(obj)

        log.info(f"Data created: {obj}")

        # DynamoService().save_item(objects, json_dict["table"])
        return f"{loops} itens saved"
    except Exception as ex:
        log.error(f"Error on saving data: {ex}")
        return ex



@app.route("/sqs", methods=['POST'])
def save_sqs():
    try:
        json_dict = request.get_json()
        loops = json_dict["amount"]
        ValidationService.check_type(loops, "int")

        objs = []

        for _ in range(loops):
            obj = OrchestratorService().process_dict(json_dict["data"])
            objs.append(obj)

        SqsService().write_sqs_batch(objs, json_dict["queue"])

        return f"{loops} itens saved"
    except Exception as ex:
        log.error(f"Error on sending message: {ex}")
        return ex

@app.route("/kafka-schema", methods=['POST'])
def produce_kafka_message_schema():
    try:
        json_dict = request.get_json()
        loops = json_dict["amount"]
        ValidationService.check_type(loops, "int")

        objs = []

        for _ in range(loops):
            obj = OrchestratorService().process_dict(json_dict["data"])
            objs.append(obj)

        KafkaService(json_dict["broker"], json_dict["schema_registry"]).send_message_schema(objs, json_dict["topic"], json_dict["subject"])

        return f"Messages were produced"
    except Exception as ex:
        log.error(f"Error on sending message: {ex}")
        return ex

@app.route("/kafka", methods=['POST'])
def produce_kafka_message():
    try:
        json_dict = request.get_json()
        loops = json_dict["amount"]
        ValidationService.check_type(loops, "int")

        objs = []

        for _ in range(loops):
            obj = OrchestratorService().process_dict(json_dict["data"])
            objs.append(obj)

        KafkaService(json_dict["broker"]).send_message(objs, json_dict["topic"])

        return f"Messages were produced"
    except Exception as ex:
        log.error(f"Error on sending message: {ex}")
        return ex


if __name__ == '__main__':
    init_logs(log.INFO)
    app.run()