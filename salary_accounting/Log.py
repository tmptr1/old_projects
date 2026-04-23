import datetime
import logging
from logging.handlers import RotatingFileHandler

MAX_LOG_ROWS = 200

class Log:
    def __init__(self, log_name, text_browser=None):
        self.text_browser = text_browser

        # self.loggers = [get_logger(l) for l in ['user_module.log', 'payment_module.log']]
        self.logger = get_logger(log_name)

        with open(log_name, 'r') as log_file:
            last_log_rows = log_file.readlines()[-MAX_LOG_ROWS:]
            if last_log_rows and self.text_browser:
                self.text_browser.append('\n'.join(l.replace('\n', '') for l in last_log_rows))

        if self.text_browser:
            self.text_browser.append("<hr><br>")

    def log(self, text):
        self.logger.log(21, str(text))
        if self.text_browser:
            self.text_browser.append(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}")



def get_logger(log_name):
    logger = logging.getLogger(log_name)
    logger.setLevel(21)
    formater = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    f_handler = RotatingFileHandler(log_name, maxBytes=5 * 1024 * 1024, backupCount=2, errors='ignore')
    f_handler.setFormatter(formater)
    # s_handler = logging.StreamHandler()
    # s_handler.setFormatter(formater)
    logger.addHandler(f_handler)
    return logger