import logging

import moviepy.editor as mpy
from gtts import gTTS
from datetime import datetime
from pydub import AudioSegment


class ArrayLengthMismatchException(Exception):
    pass


class VideoGenerator:
    __slots__ = ("__images", "__display_size", "__video_duration",
                 "__processed_images", "__with_subtitles", "__final_clip", "__video_path")

    def __init__(self, **kwargs):
        self.__images: [str] = kwargs["images"]
        self.__display_size: (int, int) = kwargs["display_size"]
        self.__video_duration: int = kwargs["video_duration"]
        self.__processed_images: [str] = []
        self.__with_subtitles = False
        self.__video_path = ""
        self.__final_clip = None

    def apply_images(self, imageclip_duration=10) -> None:
        self.__processed_images = [
            mpy.ImageClip(image).set_position("center", 0).resize(width=self.__display_size[0],
                                                                  height=self.__display_size[1])
            .set_duration(imageclip_duration)
            for image in self.__images
        ]

    def generate(self, with_subtitles=False, **kwargs):
        if len(kwargs["imageclip_start"]) != len(self.__images):
            raise ArrayLengthMismatchException("imageclip start list length is not equal to images list length")
        final_clip_elements = [image.set_position("center")
                               .set_start(kwargs["imageclip_start"][i])
                               for i, image in enumerate(self.__processed_images)]
        if with_subtitles:
            self.__with_subtitles = with_subtitles
            if len(kwargs["textclip_start"]) != len(kwargs["textclip_duration"]):
                raise ArrayLengthMismatchException("textclip_start list length is not equal to duration list length")
            if len(kwargs["textclip_start"]) != len(kwargs["paragraphs"]):
                raise ArrayLengthMismatchException("textclip_start list length is not equal to paragraphs list length")

            from moviepy.video.tools.subtitles import SubtitlesClip

            def generator(txt) -> mpy.TextClip:
                return mpy.TextClip(txt, font=kwargs["font"],
                                    fontsize=kwargs["font_size"], color=kwargs["color"], method="caption",
                                    size=(1000, 200))

            subs = [((kwargs["textclip_start"][i], kwargs["textclip_duration"][i]), paragraph)
                    for i, paragraph in enumerate(kwargs["paragraphs"])]
            subtitles = SubtitlesClip(subs, generator)
            final_clip_elements.append(subtitles.set_position(("center", "bottom")))

        self.__final_clip = (mpy.CompositeVideoClip(
            final_clip_elements, size=self.__display_size)
                             .set_duration(60)
                             )

    def save(self, filename: str, fps: int) -> None:
        self.__video_path = filename
        self.__final_clip.write_videofile(filename, fps)

    def add_audio_to_video_and_save(self, paragraphs: [str]):
        if self.__with_subtitles:
            audio_paths = []
            compiled_at = datetime.now()
            compiled_audio_path = f"audio/compiled_audio{compiled_at}.mp3"
            video_with_audio_path = f"samples/{compiled_at}--with-audio---.mp4"

            for paragraph in paragraphs:
                audio_path = f"audio/audio{datetime.now()}.mp3"
                audio_paths.append(audio_path)
                tts = gTTS(paragraph, lang='en')
                tts.save(audio_path)

            videoclip = mpy.VideoFileClip(self.__video_path)
            audioclips = [mpy.AudioFileClip(audio) for audio in audio_paths]
            final_audioclip = mpy.concatenate_audioclips(audioclips)
            final_audioclip.write_audiofile(compiled_audio_path)
            videoclip.audio = mpy.CompositeAudioClip([mpy.AudioFileClip(compiled_audio_path)])
            videoclip.write_videofile(video_with_audio_path)
        else:
            raise logging.error("No subtitles were given")


