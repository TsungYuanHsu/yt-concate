import os.path
import re

from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_videoclips

from .step import Step
from yt_concate.define_logger import logger_new


class EditVideo(Step):
    def process(self, data, inputs, utils):
        logger_new.warning('In EditVideo')
        if os.path.exists(utils.get_output_filepath(inputs['channel_id'], inputs['search_word'], inputs['limit'])):
            logger_new.warning('Concatenated video is already finished. Exit')
            return data

        clips = []
        for found in data:
            if not utils.video_file_exists(found.yt):
                continue
            try:
                t_start, t_end = self.parse_caption_time(found.time)
                video = VideoFileClip(found.yt.video_filepath).subclip(t_start, t_end)
                clips.append(video)
            except OSError as e:
                logger_new.error(f'Found error: {e}')
                continue

            if len(clips) >= inputs['limit']:
                logger_new.warning('Clip concatenation exceeds limit number, finish the process')
                break

        final_clip = concatenate_videoclips(clips)
        output_filepath = utils.get_output_filepath(inputs['channel_id'], inputs['search_word'], inputs['limit'])
        final_clip.write_videofile(output_filepath)

    def parse_caption_time(self, caption_time):
        start, end = caption_time.split(' --> ')
        return self.parse_time_str(start), self.parse_time_str(end)

    def parse_time_str(self, time):
        h, m, s, ms = re.split(r'[:,]', time)
        return int(h), int(m), int(s) + int(ms) / 1000

