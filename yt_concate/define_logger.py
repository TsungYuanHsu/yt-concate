import logging

logger_new = logging.getLogger('logger_new')
logger_new.setLevel(logging.DEBUG)

# logging into text.log
formatter = logging.Formatter('%(levelname)s:%(name)s:%(asctime)s:%(message)s')
file_handler = logging.FileHandler('test.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger_new.addHandler(file_handler)

# logging into screen
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(formatter)
logger_new.addHandler(stream_handler)
