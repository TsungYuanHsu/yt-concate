from yt_concate.define_logger import logger_new
from .step import Step



class Preflight(Step):
    def process(self, data, inputs, utils):
        logger_new.warning('In Preflight')
        utils.create_dirs()
