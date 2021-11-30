def check_type(field, typing):
    if(typing  != type(field).__name__):
        raise Exception(f"Data '{field}' is type of {type(field).__name__} and was defined as {typing}")

def check_min_max_valid(min, max):
    if (min > max):
        raise Exception("Minimum value can't not be bigger than max value")
