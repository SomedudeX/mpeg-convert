"""Metadata getter and printer functions"""

import json

from ffmpeg import FFmpeg
from rich.console import Console


class MetadataLogger:
    """The MetadataLogger()'s only purpose is to log the metadata"""

    @staticmethod
    def log_metadata(_metadata: dict) -> None:
        """Prints metadata content (stored as dict) from ffprobe"""
        _metadata = _metadata["streams"]
        Console().log(f"[Info] Start source info: ", highlight=False)

        for _stream in _metadata:
            if _stream["codec_type"] == "video":
                MetadataLogger.log_video_metadata(_stream)
            elif _stream["codec_type"] == "audio":
                MetadataLogger.log_audio_metadata(_stream)
            else:
                Console().log(f"- Auxiliary (stream type '{_stream["codec_type"]}')", highlight=False)

        Console().log(f"[Info] End source info ", highlight=False)
        return

    @staticmethod
    def log_video_metadata(_video_stream: dict) -> None:
        """Logs the video metadata of a stream onto the console
        
        + Args -
            Video_stream: a dictionary representing a video stream provided by 
            ffprobe
        """

        # The notorious 'one-liners', except 14 times
        try: _idx: str = f"{_video_stream['index']}"
        except KeyError: _idx: str = f"N/A"
        try: _col: str = f"{_video_stream['color_space']}"
        except KeyError: _col: str = f"N/A"
        try: _fmt: str = f"{_video_stream['codec_long_name']}"
        except KeyError: _fmt: str = f"N/A"
        try: _res: str = f"{_video_stream['width']}x{_video_stream['height']}"
        except KeyError: _res: str = f"N/A"
        try: _fps: str = f"{MetadataLogger._get_framerate(_video_stream['avg_frame_rate'])}"
        except KeyError: _fps: str = f"N/A"
        try: _dur: str = f"{round(float(_video_stream['duration']), 2)}"
        except KeyError: _dur: str = f"N/A"
        try: _fra: str = f"{round(float(_fps) * float(_dur), 2)}"
        except KeyError: _fra: str = f"N/A"

        Console().log(f"- Video (source stream {_idx})", highlight=False)
        Console().log(f"|    Video codec      : {_fmt}", highlight=False)
        Console().log(f"|    Video color      : {_col}", highlight=False)
        Console().log(f"|    Video resolution : {_res}", highlight=False)
        Console().log(f"|    Video framerate  : {_fps}", highlight=False)
        Console().log(f"|    Video length     : {_dur}s", highlight=False)
        Console().log(f"|    Total frames     : {_fra}", highlight=False)
        return

    @staticmethod
    def log_audio_metadata(_audio_stream: dict) -> None:
        """Logs the audio metadata of a stream
        
        + Args -
            Audio_stream: a dictionary representing an audio stream provided by 
            ffprobe
        """

        # The notorious 'one-liners', except 14 times
        try: _idx: str = f"{_audio_stream['index']}"
        except KeyError: _idx: str = f"N/A"
        try: _fmt: str = f"{_audio_stream['codec_long_name']}"
        except KeyError: _fmt: str = f"N/A"
        try: _prf: str = f"{_audio_stream['profile']}"
        except KeyError: _prf: str = f"N/A"
        try: _smp: str = f"{_audio_stream['sample_rate']} Hz"
        except KeyError: _smp: str = f"N/A"
        try: _chn: str = f"{_audio_stream['channels']}"
        except KeyError: _chn: str = f"N/A"
        try: _lay: str = f"{_audio_stream['channel_layout'].capitalize()}"
        except KeyError: _lay: str = f"N/A"
        try: _btr: str = f"{int(_audio_stream['bit_rate']) // 1000} kb/s"
        except KeyError: _btr: str = f"N/A"

        Console().log(f"- Audio (source stream {_idx})", highlight=False)
        Console().log(f"|    Audio codec      : {_fmt}", highlight=False)
        Console().log(f"|    Audio profile    : {_prf}", highlight=False)
        Console().log(f"|    Audio samplerate : {_smp}", highlight=False)
        Console().log(f"|    Audio channels   : {_chn}", highlight=False)
        Console().log(f"|    Audio layout     : {_lay}", highlight=False)
        Console().log(f"|    Audio bitrate    : {_btr}", highlight=False)
        return

    @staticmethod
    def _get_framerate(_fps: str) -> str:   # Static overload for MetadataManager::get_framerate()
        _numerator = ""                     # It is a member of MetadataLogger because python does
        for _ in range(len(_fps)):          # not support function overloading. See get_framerate()
            if _fps[0] != "/":              # method from class MetadataManager for docs if you are
                _numerator += _fps[0]       # contributing
                _fps = _fps[1:]
                continue
            _fps = _fps[1:]
            break

        _denominator = _fps

        _numerator = float(_numerator)
        _denominator = float(_denominator)
        return str(round(_numerator / _denominator, 2))


class MetadataManager:
    """The MetadataManager() class represents a media's metadata"""

    def __init__(
            self,
            _input_path: str,
            _debug: bool = False
    ) -> None:
        """Initializes an instance of `MediaManager`"""
        self.video_stream = None
        self.audio_stream = None
        self.metadata = {}

        self.console = Console(highlight=False)

        self.input_path = _input_path
        self.get_metadata(_debug)
        return

    def get_metadata(
            self,
            _debug: bool = False
    ) -> None:
        """Gets the metadata of the media file that the object is
        currently representing. This method also loads the audio_stream
        and video_stream attributes, which represents the first
        video/audio stream the program encounters
        """
        self.console.log("[Info] Probing file properties and metadata with ffprobe")
        _ffprobe = FFmpeg(executable="ffprobe").input(
            self.input_path,
            print_format='json',
            show_streams=None
        )

        @_ffprobe.on("stderr")
        def show_cout(_msg: str) -> None:
            if _debug:
                self.console.log(f"[FFprobe] {_msg}")

        self.metadata: dict = json.loads(_ffprobe.execute())

        self.audio_stream = self.get_audio_stream()
        self.video_stream = self.get_video_stream()
        return

    def get_audio_stream(self) -> int:
        """Gets the index of the first audio stream in self.metadata. If
        multiple streams are present, the first stream is returned, and
        the rest of the streams are ignored
        
        If no audio streams are present in the metadata, the function 
        returns -1. 
        """
        _ret: int = -1
        for _stream in self.metadata["streams"]:
            if _stream["codec_type"] == "audio":
                self.console.log(f"[Info] Using first audio stream found (stream {_stream["index"]})")
                _ret = _stream["index"]
                break

        if _ret == -1:
            self.console.log(f"[yellow][Warning] No audio stream found")
        return _ret

    def get_video_stream(self) -> int:
        """Gets the index of the first video stream in self.metadata. If
        multiple streams are present, the first stream is returned, and
        the rest of the streams are ignored
        
        If no video streams are present in the metadata, the function 
        returns -1. 
        """
        _ret: int = -1
        for _stream in self.metadata["streams"]:
            if _stream["codec_type"] == "video":
                self.console.log(f"[Info] Using first video stream found (stream {_stream["index"]})")
                _ret = _stream["index"]
                break

        if _ret == -1:
            self.console.log(f"[yellow][Warning] No video stream found")
        return _ret

    def get_total_secs(self) -> int:
        """Gets the total length (in seconds) of the first video stream"""
        _ret = self.metadata["streams"][self.video_stream]["duration"]
        _ret = float(_ret)
        return int(_ret)

    def get_framerate(self) -> int:
        """Gets the average framerate of the first video stream. Because
        the framerate is stored as a fraction in ffprobe, and some
        framerate are not whole numbers, this method has to manually parse
        the framerate by doing division in order to get the framerate as a
        floating-point integer
        
        """
        _fps: str = self.metadata["streams"][self.video_stream]["avg_frame_rate"]

        _numerator = ""
        for _ in range(len(_fps)):
            if _fps[0] != "/":
                _numerator += _fps[0]
                _fps = _fps[1:]
                continue
            _fps = _fps[1:]
            break

        _denominator = _fps

        _numerator = float(_numerator)
        _denominator = float(_denominator)
        return int(_numerator // _denominator)
