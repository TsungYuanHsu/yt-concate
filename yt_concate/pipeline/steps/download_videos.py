import os
from multiprocessing import Process
import time

from pytube import YouTube

from .step import Step
from yt_concate.settings import VIDEOS_DIR
from yt_concate.define_logger import logger_new


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        logger_new.warning('In DownloadVideos')
        start = time.time()
        yt_set = set([found.yt for found in data])
        logger_new.info(f'Videos to download: {len(yt_set)}')

        # # use single thread to download videos
        # for yt in yt_set:
        #     url = yt.url
        #     if utils.video_file_exists(yt):
        #         logger_new.info(f'Found existing video file for {url}, skipping')
        #         continue
        #     logger_new.info(f'Downloading {url}')
        #     YouTube(url).streams.filter(res="720p").first().download(output_path=VIDEOS_DIR, filename=yt.id + '.mp4')

        # use multiprocessing to download videos
        self.activate_multiprocessing_videos(yt_set, inputs, utils)

        end = time.time()
        logger_new.warning(f'Multi-processing downloading videos takes {end - start} seconds')
        return data

    def download_videos(self, yt_set, inputs, utils):
        for yt in yt_set:
            url = yt.url
            if utils.video_file_exists(yt):
                logger_new.info(f'Found existing video file for {url}, skipping')
                continue
            if len(os.listdir(VIDEOS_DIR)) > inputs['limit']:
                logger_new.info('Enough videos, skip')
                break
            logger_new.info(f'Downloading {url}')
            YouTube(url).streams.filter(res="720p").first().download(output_path=VIDEOS_DIR, filename=yt.id + '.mp4')

    def activate_multiprocessing_videos(self, yt_set, inputs, utils):
        processes = []
        section = int(len(yt_set) / 4)
        for i in range(4):
            start = int(i * section)
            end = int((i + 1) * section)
            processes.append(Process(target=self.download_videos, args=(list(yt_set)[start:end], inputs, utils)))

        for process in processes:
            process.start()

        for process in processes:
            process.join()
