import logging
from .config import LOGS_PATH

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOGS_PATH)
        ]
    )

def get_logger(name):
    return logging.getLogger(name)
