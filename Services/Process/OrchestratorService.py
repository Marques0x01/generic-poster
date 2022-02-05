from Services.Process.GeneratorService import GeneratorService
import logging as log
from Services.Process.ValidationService import ValidationService
class OrchestratorService:

    def process_dict(self, data):
        obj = {}
        try:
            for item in data:
                
                ValidationService.check_null(item["type"], "type")
                ValidationService.check_null(item["name"], "name")

                item["field_config"] = {} if not ValidationService.field_exists(item, "field_config") else item["field_config"]
                    
                item["field_config"]["type"] = item["type"]

                if ValidationService.field_exists(item, "default"):
                    obj[item["name"]] = GeneratorService.generate_default_value(
                        item)
                    continue

                if ValidationService.field_exists(item, "possibilities"):
                    ValidationService.check_type(item["possibilities"], list)
                    if len(item["possibilities"]) > 0:
                        obj[item["name"]] = GeneratorService.generate_random_possibility(
                            item["possibilities"], item["field_config"]["type"])
                        continue
                    log.warn(f"There is not 'possibilities' to choose... Generating random value for {item['name']}")

                obj[item["name"]] = GeneratorService().generate_random_value(field_config=item["field_config"])
            return obj
        except Exception as ex:
            log.error(f"Error on processing: {ex}")
            raise ex