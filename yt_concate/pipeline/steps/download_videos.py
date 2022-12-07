import os
from multiprocessing import Process
import time

from pytube import YouTube

from .step import Step
from yt_concate.settings import VIDEOS_DIR


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        yt_set = set([found.yt for found in data])
        print('Videos to download:', len(yt_set))

        if len(os.listdir(VIDEOS_DIR)) > 30:
            print('Enough videos, skip')
            return data

        # # use single thread to download videos
        # for yt in yt_set:
        #     url = yt.url
        #     if utils.video_file_exists(yt):
        #         print(f'Found existing video file for {url}, skipping')
        #         continue
        #     print('Downloading', url)
        #     YouTube(url).streams.filter(res="720p").first().download(output_path=VIDEOS_DIR, filename=yt.id + '.mp4')

        # use multiprocessing to download videos
        self.activate_multiprocessing_videos(yt_set, inputs, utils)

        end = time.time()
        print('Multi-processing downloading videos takes', end - start, 'seconds')
        return data

    def download_videos(self, yt_set, inputs, utils):
        for yt in yt_set:
            url = yt.url
            if utils.video_file_exists(yt):
                print(f'Found existing video file for {url}, skipping')
                continue
            print('Downloading', url)
            YouTube(url).streams.filter(res="720p").first().download(output_path=VIDEOS_DIR, filename=yt.id + '.mp4')

    def activate_multiprocessing_videos(self, yt_set, inputs, utils):
        processes = []
        section = int(len(yt_set) / 4)
        for i in range(4):
            start = int(i * section)
            end = int((i+1) * section)
            processes.append(Process(target=self.download_videos, args=(list(yt_set)[start:end], inputs, utils)))

        for process in processes:
            process.start()

        for process in processes:
            process.join()
