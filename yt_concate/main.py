import sys
sys.path.append('../')
import getopt

from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.pipeline.steps.preflight import Preflight
from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.download_captions import DownloadCaptions
from yt_concate.pipeline.steps.read_caption import ReadCaption
from yt_concate.pipeline.steps.search import Search
from yt_concate.pipeline.steps.download_videos import DownloadVideos
from yt_concate.pipeline.steps.edit_video import EditVideo
from yt_concate.pipeline.steps.postflight import Postflight
from yt_concate.define_logger import logger_new
from yt_concate.utils import Utils

CHANNEL_ID = 'UCKSVUHI9rbbkXhvAXK-2uxA'


def main():
    logger_new.warning('Enter main.py')
    inputs = {
        'channel_id': CHANNEL_ID,
        'search_word': 'incredible',
        'limit': 15,
        'cleanup': True,
    }

    # command line arguments
    short_opts = 'hc:s:l:cls:ll:'
    long_opts = 'help channel_id= search_word= limit= cleanup= logging_level='.split()
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        logger_new.info('python main.py test.py -c <channel_id> -s <search_word> -l <limit>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            logger_new.info('python main.py test.py -c <channel_id> -s <search_word> -l <limit>')
            sys.exit()
        elif opt in ("-c", "--channel_id"):
            inputs['channel_id'] = arg
        elif opt in ("-s", "--search_word"):
            inputs['search_word'] = arg
        elif opt in ("-l", "--limit"):
            inputs['limit'] = int(arg)
        elif opt in ("-cls", "--cleanup"):
            inputs['cleanup'] = bool(arg)

    logger_new.warning("Run main.py\n"
                       "Running condition:\n"
                       f"channel_id is {inputs['channel_id']}\n"
                       f"search_word is {inputs['search_word']}\n"
                       f"video concatenation limit is {inputs['limit']}\n"
                       f"Auto cleanup is {inputs['cleanup']}\n"
                       )


    steps = [
        Preflight(),
        GetVideoList(),
        InitializeYT(),
        DownloadCaptions(),
        ReadCaption(),
        Search(),
        DownloadVideos(),
        EditVideo(),
        Postflight(),
    ]
    utils = Utils()
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()
