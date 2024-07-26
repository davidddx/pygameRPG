import logging
import sys
logfile = "projectDebug.log"
with open(logfile, 'w'):  # truncates file if there is contents in it
    pass
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler(logfile)
consoleHandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

fileHandler.setFormatter(formatter)
consoleHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)
try:
    logger.info('LOGGER HAS BEEN INITIALIZED')
except Exception as e:
    print(f"Error during logging: {e}")
