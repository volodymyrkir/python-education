import logging
from time import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("log")
f_handler = logging.FileHandler("time.log")
f_handler.setLevel(logging.INFO)
f_formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%H:%M:%S')
f_handler.setFormatter(f_formatter)
logger.addHandler(f_handler)


def log(func):
    def inner(*args, **kwargs):
        start = time()
        ans = func(*args, **kwargs)
        end = time()
        logger.info(f"Function {func} execution took {end - start} time with arguments {args} {kwargs}")
        return ans

    return inner
