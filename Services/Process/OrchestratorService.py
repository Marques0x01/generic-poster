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

                if ValidationService.field_exists(item, "default"):
                    obj[item["name"]] = GeneratorService.generate_default_value(item)
                    continue

                if ValidationService.field_exists(item, "possibilities"):
                    ValidationService.check_type(item["possibilities"], "list")
                    if len(item["possibilities"]) > 0:
                        obj[item["name"]] = GeneratorService.generate_random_possibility(
                            item["possibilities"], item["type"])
                        continue
                    log.warn(f"There is not 'possibilities' to choose... Generating random value for {item['name']}")

                if ("is_null" in item and item["is_null"] is not None and item["is_null"]):
                    return None

                obj[item["name"]] = GeneratorService().generate_random_value(item)
            return obj
        except Exception as ex:
            log.error(f"Error on processing: {ex}")
            raise ex