import logging
import os
import re


def get_logger(name: str, level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(level)
    os.makedirs("./logs", exist_ok=True)
    fh = logging.FileHandler(os.path.join("./logs/", name+".log"), mode='a')
    fh.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def check_url(url: str):
    pattern = re.compile(
        r"(^([hH][tT]{2}[pP]:\/\/|[hH][tT]{2}[pP][sS]:\/\/))([w]{3}\.)?(([A-Za-z0-9-~]+)\.)+([A-Za-z0-9-~\/])+")
    result = pattern.match(url)
    if result is not None:
        return True
    else:
        return False
