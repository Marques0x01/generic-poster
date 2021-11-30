from flask import Flask, request
import Services.Process.orchestrator as orchestrator
import Services.Process.validations as validation
import Services.Dynamo.dynamo_service as dynamo
import Services.Sqs.sqs_service as sqs

app = Flask(__name__)


@app.route("/dynamo", methods=['POST'])
def save_dynamo():
    try:
        json_dict = request.get_json()
        loops = json_dict["amount"]
        validation.check_type(loops, "int")

        objects = []

        for number in range(loops):
            obj = orchestrator.process_dict(json_dict["data"])
            objects.append(obj)

        dynamo.save_item(objects, json_dict["table"])
        return f"{loops} itens saved"
    except:
        raise



@app.route("/sqs", methods=['POST'])
def save_sqs():
    try:
        json_dict = request.get_json()
        loops = json_dict["amount"]
        validation.check_type(loops, "int")

        for number in range(loops):
            obj = orchestrator.process_dict(json_dict["data"])
            response_id = sqs.send_sqs(obj, json_dict["queue"])
            print(f"Posted: {number + 1} - ID: {response_id}")

        return f"{loops} itens saved"
    except:
        raise


if __name__ == '__main__':
    app.run()