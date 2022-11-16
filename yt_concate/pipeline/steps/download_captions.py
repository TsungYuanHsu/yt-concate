import time

from pytube import YouTube

from .step import Step
from .step import StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()

        for yt in data:
            print('Downloading caption for', yt.id)
            if utils.caption_file_exists(yt):
                print(f'found existing file: {yt.url}')
                continue

            try:
                source = YouTube(yt.url)
                en_caption = source.captions.get_by_language_code('a.en')
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            except (KeyError, AttributeError):
                print('Error when downloading caption for', yt.url)
                continue

            text_file = open(utils.get_caption_filepath(yt.url), "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()

        end = time.time()
        print('took', end - start, 'seconds in downloading captions')

        return data
