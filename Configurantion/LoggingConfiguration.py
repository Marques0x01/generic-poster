import logging

def init_logs(log_level):
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.setLevel(log_level)
    else:
        logging.basicConfig(level=log_level)