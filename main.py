from mimetypes import init
from flask import Flask, request
from Services.Process.OrchestratorService import OrchestratorService
from Services.Process.ValidationService import ValidationService
from Services.Dynamo.DynamoService import DynamoService
from Services.Sqs.SqsService import SqsService
import logging as log
from Configurantion.LoggingConfiguration import init_logs


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

        DynamoService().save_item(objects, json_dict["table"])
        return f"{loops} itens saved"
    except Exception as ex:
        log.error(f"Error on saving data: {ex}")



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


if __name__ == '__main__':
    init_logs(log.INFO)
    app.run()