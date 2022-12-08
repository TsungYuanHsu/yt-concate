from .step import Step
from yt_concate.model.yt import YT
from yt_concate.define_logger import logger_new

class InitializeYT(Step):
    def process(self, data, inputs, utils):
        logger_new.warning('In InitializeYT')
        return [YT(url) for url in data]
