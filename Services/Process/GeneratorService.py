import random
import string
import datetime
from Services.Process.ValidationService import ValidationService
import logging as log

class GeneratorService:

    def generate_random_possibility(self, possibilities, typing):
        try:
            value = random.choice(possibilities)
            ValidationService.check_type(value, typing)
            return value
        except Exception as ex:
            log.error(f"Error on creating random value: {ex}")
            raise ex

    def generate_default_value(self, item):
        try:
            ValidationService.check_type(item["default"], item["field_config"]["type"])
            return item["default"]
        except Exception as ex:
            log.error(f"Error on creating default value: {ex}")
            raise ex

    def generate_random_value(self, field_config):
        try:
            return {
                'str': self.__generate_string,
                'string': self.__generate_string,
                'int': self.__generate_integer,
                'integer': self.__generate_integer,
                'number': self.__generate_integer,
                'bool': self.__generate_boolean,
                'boolean': self.__generate_boolean,
                'float': self.__generate_double,
                'double': self.__generate_double,
                'date': self.__generate_date,
                'object': self.__generate_object,
                'array': self.__generate_array
            }.get(field_config["type"], None)(field_config)
        except Exception as ex:
            log.error(f"Error on creating value: {ex}")
            raise ex


    def __generate_string(self, field_config):
        try:
            letters = string.ascii_lowercase if "lower_case" not in field_config or field_config["lower_case"] is None or field_config[
                "lower_case"] else string.ascii_uppercase

            if ValidationService.field_exists(field_config, "amount_chars"):
                if field_config["amount_chars"] > 0:
                    return ''.join(random.choice(letters) for _ in range(field_config["amount_chars"]))
                log.warn("String amount chars configured less than zero")

            return ''.join(random.choice(letters) for _ in range(50))
        except Exception as ex:
            log.error(f"Error on creating string: {ex}")
            raise ex

    def __generate_integer(self, field_config):
        try:
            min = 0 if not ValidationService.field_exists(field_config, "min") else field_config["min"]
            max = 1000000 if not ValidationService.field_exists(field_config, "max") else field_config["max"]
            ValidationService.check_min_max_valid(min, max)
            return random.randint(min, max)
        except Exception as ex:
            log.error(f"Error on creating integer: {ex}")
            raise ex

    def __generate_double(self, field_config):
        try:
            min = 0 if not ValidationService.field_exists(field_config, "min") else field_config["min"]
            max = 1000000 if not ValidationService.field_exists(field_config, "max") else field_config["max"]
            ValidationService.check_min_max_valid(min, max)
            return "{:.2f}".format(random.uniform(min, max))
        except Exception as ex:
            log.error(f"Error on creating double: {ex}")
            raise ex

    def __generate_boolean(self, field_config):
        try:
            return bool(random.getrandbits(1))
        except Exception as ex:
            log.error(f"Error on creating boolean: {ex}")
            raise ex

    def __generate_date(self, field_config):
        try:
            date = self.__generate_random_date(field_config)
            if ValidationService.field_exists(field_config, "with_time") and field_config["with_time"]:
                time = self.__generate_random_time(field_config["time"])
                date = date + time
            else:
                date = date.date()

            if ValidationService.field_exists(field_config, "as_string") and field_config["as_string"]:
                date = str(date)

            return date
        except Exception as ex:
            log.error(f"Error on creating date: {ex}")
            raise ex

    def __generate_random_date(self, field_config):

        if not ValidationService.field_exists(field_config, "date"):
            return self.__generate_random_default_date()

        date = field_config["date"]

        if not ValidationService.field_exists(field_config, "year"):
            year = self.__generate_year(1500, 2500)
        else:
            year = self.__generate_year(date["year"]["min"], date["year"]["max"])

        if not ValidationService.field_exists(field_config, "year"):
            month = self.__generate_year(1, 12)
        else:
            month = self.__generate_month(date["month"]["min"], date["month"]["max"])

        if not ValidationService.field_exists(field_config, "year"):
            month = self.__generate_year(1, 30)
        else:
            if month == 2 and ValidationService.field_exists(field_config, "year") and date["day"]["max"] > 28:
                date["day"]["max"] = 28

            day = self.__generate_day(date["day"]["min"], date["day"]["max"])

        return datetime.datetime(year, month, day, 0, 0, 0)

    def __generate_random_default_date(self):
        year = self.__generate_year(1500, 2500)
        month = self.__generate_month(1, 12)

        day = self.__generate_day(1, 28)

        return datetime.datetime(year, month, day, 0, 0, 0)

    def __generate_year(self, min, max):
        min_year = 0 if min < 0 or min is None \
            else min

        min_year = 9999 if min > 9999 \
            else min_year

        max_year = 0 if max < 0 or max is None \
            else max

        max_year = 9999 if max > 9999 \
            else max_year

        return random.randint(min_year, max_year)

    def __generate_month(self, min, max):
        min_month = 1 if min <= 0 or min is None \
            else min

        min_month = 12 if min > 12 \
            else min_month

        max_month = 1 if max <= 0 or max is None \
            else max

        max_month = 12 if max > 12 \
            else max_month

        return random.randint(min_month, max_month)

    def __generate_day(self, min, max):
        min_day = 1 if min <= 0 or min is None \
            else min

        min_day = 30 if min > 30 \
            else min_day

        max_day = 1 if max <= 0 or max is None \
            else max

        max_day = 30 if max > 30 \
            else max_day

        return random.randint(min_day, max_day)

    def __generate_random_time(self, field_config):
        if not ValidationService.field_exists(field_config, "time"):
            return self.__generate_random_default_time()

        time = field_config["time"]

        if not ValidationService.field_exists(field_config, "hours"):
            hour = self.__generate_hours(0, 23)
        else:
            hour = self.__generate_hours(time["hours"]["min"], time["hours"]["max"])

        if not ValidationService.field_exists(field_config, "hours"):
            minute = self.__generate_hours(0, 59)
        else:
            minute = self.__generate_time(time["minutes"]["min"], time["minutes"]["max"])
        if not ValidationService.field_exists(field_config, "hours"):
            second = self.__generate_hours(0, 59)
        else:
            second = self.__generate_time(time["seconds"]["min"], time["seconds"]["max"])

        return datetime.timedelta(hours=hour, minutes=minute, seconds=second)

    def __generate_random_default_time(self):
        hour = self.__generate_hours(0, 23)
        minute = self.__generate_time(0, 59)
        second = self.__generate_time(0, 59)
        return datetime.timedelta(hours=hour, minutes=minute, seconds=second)

    def __generate_hours(self, min, max):
        min_hour = 0 if min < 0 or min is None \
            else min

        min_hour = 23 if min > 23 \
            else min_hour

        max_hour = 0 if max < 0 or max is None \
            else max

        max_hour = 23 if max > 23 \
            else max_hour

        return random.randint(min_hour, max_hour)

    def __generate_time(self, min, max):
        min_time = 0 if min < 0 or min is None \
            else min

        min_time = 59 if min > 59 \
            else min_time

        max_time = 0 if max < 0 or max is None \
            else max

        max_time = 59 if max > 59 \
            else max_time

        return random.randint(min_time, max_time)

    def __generate_object(self, fields_config):
        try:
            obj = {}
            for field in fields_config["fields"]:

                if not ValidationService.field_exists(field, "field_config"):
                    field["field_config"] = {}    

                field["field_config"]["type"] = field["type"]

                if ValidationService.field_exists(field, "default"):
                    obj[field["name"]] = self.generate_default_value(field)
                    continue

                if ValidationService.field_exists(field, "possibilities"):
                    ValidationService.check_type(field["possibilities"], list)
                    if len(field["possibilities"]) > 0:
                        obj[field["name"]] = self.generate_random_possibility(
                            field["possibilities"], field["field_config"]["type"])
                        continue
                    log.warn(f"There is not 'possibilities' to choose... Generating random value for {item['name']}")

                obj[field["name"]] = self.generate_random_value(field["field_config"])
            return obj
        except Exception as ex:
            log.error(f"Error on creating object: {ex}")
            raise ex

    def __generate_array(self, field_config):
        try:
            arr = []

            if not ValidationService.field_exists:
                return arr

            ValidationService.check_type(field_config["amount"], "int")
        
            for _ in range(field_config["amount"]):
                arr.append(self.generate_random_value(
                    field_config["array_data_config"]))
            return arr
        except Exception as ex:
            log.error(f"Error on creating array: {ex}")
            raise ex
