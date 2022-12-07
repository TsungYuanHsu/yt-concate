import time
from multiprocessing import Process

from pytube import YouTube

from .step import Step
from .step import StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()

        # # use single thread to download captions
        # for yt in data:
        #     print('Downloading caption for', yt.id)
        #     if utils.caption_file_exists(yt):
        #         print(f'found existing file: {yt.url}')
        #         continue
        #
        #     try:
        #         source = YouTube(yt.url)
        #         en_caption = source.captions.get_by_language_code('a.en')
        #         en_caption_convert_to_srt = (en_caption.generate_srt_captions())
        #     except (KeyError, AttributeError):
        #         print('Error when downloading caption for', yt.url)
        #         continue
        #
        #     text_file = open(yt.caption_filepath, "w", encoding='utf-8')
        #     text_file.write(en_caption_convert_to_srt)
        #     text_file.close()

        # use multi-processing to download captions
        self.activate_multiprocessing_captions(data, inputs, utils)

        end = time.time()
        print('Multi-processing downloading captions takes', end - start, 'seconds')

        return data

    def download_captions(self, data, inputs, utils):
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

            text_file = open(yt.caption_filepath, "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()

    def activate_multiprocessing_captions(self, data, inputs, utils):
        processes = []
        section = int(len(data) / 4)
        for i in range(4):
            start = int(i * section)
            end = int((i+1) * section)
            processes.append(Process(target=self.download_captions, args=(data[start:end], inputs, utils)))

        for process in processes:
            process.start()

        for process in processes:
            process.join()

