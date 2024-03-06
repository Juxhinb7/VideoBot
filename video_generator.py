import moviepy.editor as mpy


class ArrayLengthMismatchException(Exception):
    pass


class VideoGenerator:
    __slots__ = ("__images", "__display_size", "__video_duration",
                 "__processed_images", "__final_clip")

    def __init__(self, **kwargs):
        self.__images: [str] = kwargs["images"]
        self.__display_size: (int, int) = kwargs["display_size"]
        self.__video_duration: int = kwargs["video_duration"]
        self.__processed_images: [str] = []
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
            if len(kwargs["textclip_start"]) != len(kwargs["textclip_duration"]):
                raise ArrayLengthMismatchException("start list length is not equal to duration list length")
            if len(kwargs["textclip_start"]) != len(kwargs["paragraphs"]):
                raise ArrayLengthMismatchException("start list length is not equal to paragraphs list length")

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
        self.__final_clip.write_videofile(filename, fps)
