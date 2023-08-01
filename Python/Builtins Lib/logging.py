# https://realpython.com/python-logging/

import logging
from time import sleep

LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)
for handler in LOG.handlers:
    LOG.removeHandler(handler)

# LOG.addHandler(ColorHandler())

grey = "\x1b[38;20m"
yellow = "\x1b[33;20m"
red = "\x1b[31;20m"
bold_red = "\x1b[31;1m"
reset = "\x1b[0m"

# LOG.debug(grey + 'hello!' + reset)
LOG.critical(grey + 'hello!' + reset)

# while True:
#     LOG.critical('hello!')
#     sleep(0.1)
