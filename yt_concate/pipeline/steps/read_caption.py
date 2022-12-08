from yt_concate.pipeline.steps.step import Step
from yt_concate.define_logger import logger_new

class ReadCaption(Step):
    def process(self, data, inputs, utils):
        logger_new.warning('In ReadCaption')
        for yt in data:
            if not utils.caption_file_exists(yt):
                continue
            captions = {}
            with open(yt.caption_filepath, 'r', encoding='utf-8') as f:
                time = None
                caption = None
                time_line = False
                for line in f:
                    if '-->' in line:
                        time_line = True
                        time = line.strip()
                        continue
                    if time_line:
                        caption = line.strip()
                        captions[caption] = time
                        time_line = False
            yt.captions = captions

        return data
