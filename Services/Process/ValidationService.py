

from queue import Empty


class ValidationService:
    def check_type(field, typing):
        if(typing != type(field).__name__):
            raise Exception(
                f"Data '{field}' is type of {type(field).__name__} and was defined as {typing}")

    def check_min_max_valid(min, max):
        if (min > max):
            raise Exception("Minimum value can't not be bigger than max value")

    def check_null(field, field_name):
        if field is None or field is Empty:
            raise Exception(f"{field_name} can't be null")

    def field_exists(field, field_name):
        return True if field_name in field and field[field_name] is not None and field[field_name] is not Empty else False
            
    