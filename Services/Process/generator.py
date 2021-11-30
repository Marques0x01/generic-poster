import random
import string
import datetime
from Services.Process import validations


def generate_random_possibility(possibilities, typing):
    value = random.choice(possibilities)
    validations.check_type(value, typing)
    return value


def generate_default_value(item):
    validations.check_type(item["default"], item["field_config"]["type"])
    return item["default"]


def generate_random_value(field_config):
    return {
        'str': generate_string,
        'string': generate_string,
        'int': generate_integer,
        'integer': generate_integer,
        'number': generate_integer,
        'bool': generate_boolean,
        'boolean': generate_boolean,
        'float': generate_double,
        'double': generate_double,
        'date': generate_date,
        'object': generate_object,
        'array': generate_array
    }.get(field_config["type"], None)(field_config)


def generate_string(field_config):
    letters = string.ascii_lowercase if field_config["lower_case"] is None or field_config[
        "lower_case"] else string.ascii_uppercase

    if field_config["amount_chars"] is not None:
        return ''.join(random.choice(letters) for _ in range(field_config["amount_chars"]))

    return ''.join(random.choice(letters) for _ in range(50))


def generate_integer(field_config):
    min = 0 if field_config["min"] is None else field_config["min"]
    max = 1000000 if field_config["max"] is None else field_config["max"]
    validations.check_min_max_valid(min, max)
    return random.randint(min, max)


def generate_double(field_config):
    min = 0 if field_config["min"] is None else field_config["min"]
    max = 1000000 if field_config["max"] is None else field_config["max"]
    validations.check_min_max_valid(min, max)
    return "{:.2f}".format(random.uniform(min, max))


def generate_boolean(field_config):
    return bool(random.getrandbits(1))


def generate_date(field_config):
    date = generate_random_date(field_config["date"])
    if field_config["with_time"] is not None and field_config["with_time"]:
        time = generate_random_time(field_config["time"])
        date = date + time
    else:
        date = date.date()

    if field_config["as_string"] is not None and field_config["as_string"]:
        date = str(date)

    return date


def generate_random_date(date):
    year = generate_year(date["year"]["min"], date["year"]["max"])
    month = generate_month(date["month"]["min"], date["month"]["max"])

    if month == 2 and date["day"]["max"] > 28:
        date["day"]["max"] = 28

    day = generate_day(date["day"]["min"], date["day"]["max"])

    return datetime.datetime(year, month, day, 0, 0, 0)


def generate_year(min, max):
    min_year = 0 if min < 0 or min is None \
        else min

    min_year = 9999 if min > 9999 \
        else min_year

    max_year = 0 if max < 0 or max is None \
        else max

    max_year = 9999 if max > 9999 \
        else max_year

    return random.randint(min_year, max_year)


def generate_month(min, max):
    min_month = 1 if min <= 0 or min is None \
        else min

    min_month = 12 if min > 12 \
        else min_month

    max_month = 1 if max <= 0 or max is None \
        else max

    max_month = 12 if max > 12 \
        else max_month

    return random.randint(min_month, max_month)


def generate_day(min, max):
    min_day = 1 if min <= 0 or min is None \
        else min

    min_day = 30 if min > 30 \
        else min_day

    max_day = 1 if max <= 0 or max is None \
        else max

    max_day = 30 if max > 30 \
        else max_day

    return random.randint(min_day, max_day)


def generate_random_time(time):
    hour = generate_hours(time["hours"]["min"], time["hours"]["max"])
    minute = generate_time(time["minutes"]["min"], time["minutes"]["max"])
    second = generate_time(time["seconds"]["min"], time["seconds"]["max"])
    return datetime.timedelta(hours=hour, minutes=minute, seconds=second)


def generate_hours(min, max):
    min_hour = 0 if min < 0 or min is None \
        else min

    min_hour = 23 if min > 23 \
        else min_hour

    max_hour = 0 if max < 0 or max is None \
        else max

    max_hour = 23 if max > 23 \
        else max_hour

    return random.randint(min_hour, max_hour)


def generate_time(min, max):
    min_time = 0 if min < 0 or min is None \
        else min

    min_time = 59 if min > 59 \
        else min_time

    max_time = 0 if max < 0 or max is None \
        else max

    max_time = 59 if max > 59 \
        else max_time

    return random.randint(min_time, max_time)


def generate_object(fields):
    obj = {}
    for field in fields["fields"]:
        if field["default"] is not None:
            obj[field["name"]] = generate_default_value(field)
            return

        if (len(field["possibilities"]) > 0):
            obj[field["name"]] = generate_random_possibility(field["possibilities"], field["field_config"]["type"])
            return

        obj[field["name"]] = generate_random_value(field["field_config"])
    return obj


def generate_array(field_config):
    arr = []
    validations.check_type(field_config["amount"], "int")
    for number in range(field_config["amount"]):
        arr.append(generate_random_value(field_config["array_data_config"]))
    return arr
