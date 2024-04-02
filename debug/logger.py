import logging

logfile = "projectDebug.log"
with open(logfile, 'w'):  # truncates file if there is contents in it
    pass
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG
                )
handler = logging.FileHandler(logfile)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)
try:
    logger.info('LOGGER HAS BEEN INITIALIZED')
except Exception as e:
    print(f"Error during logging: {e}")