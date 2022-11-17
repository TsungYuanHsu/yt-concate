from pytube import YouTube

from .step import Step
from yt_concate.settings import VIDEOS_DIR


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        yt_set = set([found.yt for found in data])
        print('Videos to download:', len(yt_set))
        for yt in yt_set:
            url = yt.url
            if utils.video_file_exists(yt):
                print(f'Found existing video file for {url}, skipping')
                continue
            print('Downloading', url)
            YouTube(url).streams.filter(res="720p").first().download(output_path=VIDEOS_DIR, filename=yt.id + '.mp4')

        return data
