import logging

logger = logging.getLogger('linked_census')
ch = logging.StreamHandler()
logger.addHandler(ch)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
