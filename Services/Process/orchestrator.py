from Services.Process import generator


def process_dict(data):
    obj = {}
    for item in data:
        if item["default"] is not None:
            obj[item["name"]] = generator.generate_default_value(item)
            return

        if (len(item["possibilities"]) > 0):
            obj[item["name"]] = generator.generate_random_possibility(item["possibilities"], item["field_config"]["type"])
            return

        obj[item["name"]] = generator.generate_random_value(item["field_config"])
    return obj
