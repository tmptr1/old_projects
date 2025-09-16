import logging
from logging.handlers import RotatingFileHandler

def configure_logging(logger, name, level=logging.INFO):
    if not isinstance(logger, logging.Logger):
        return
    log_format = logging.Formatter("[%(asctime)s] %(module)15s:%(levelname)s - %(message)s",
                                   datefmt="%Y-%m-%d %H:%M:%S")
    handler = RotatingFileHandler(name, maxBytes=20 * 1024 * 1024, backupCount=2, errors='ignore')
    handler.setFormatter(log_format)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)