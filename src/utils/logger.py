import logging
import json
from logging.handlers import RotatingFileHandler


def get_logger(log_file):
    logger = logging.getLogger(log_file)
    logger.setLevel(logging.INFO)
    
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "event": record.msg
        }
        return json.dumps(log_record)

def get_json_logger(log_file):
    logger = logging.getLogger(log_file)
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(log_file,maxBytes=5_00_000,backupCount=5)
    
    handler.setFormatter(JSONFormatter())
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger