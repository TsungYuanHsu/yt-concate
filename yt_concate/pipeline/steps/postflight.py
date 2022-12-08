import shutil

from .step import Step
from yt_concate.settings import VIDEOS_DIR
from yt_concate.settings import CAPTIONS_DIR
from yt_concate.define_logger import logger_new


class Postflight(Step):
    def process(self, data, inputs, utils):
        logger_new.warning('In Postflight')
        logger_new.info('Delete captions directory and videos directory')
        self.remove_dirs(inputs)
        logger_new.warning('exit main.py')

    def remove_dirs(self, inputs):
        if inputs['cleanup']:
            shutil.rmtree(VIDEOS_DIR, ignore_errors=True)
            shutil.rmtree(CAPTIONS_DIR, ignore_errors=True)

