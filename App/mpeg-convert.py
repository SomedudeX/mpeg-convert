#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file uses the following styles for token names: 
#     PascalCase       Class name
#     snake_case       Variable or function/method name
#     _underscore      Variable/function should be used only intenally in
#                      the scope it's declared in (and should not be
#                      modified by the end user)
#
# Notes: 
#     Because python does not have a reliable way of signalling the end
#     of a particular scope, method, or class, any class/method in this 
#     file will always terminate in `return` regardless of the return
#     type. 
#
# This file uses 4 spaces for indentation. 


import os
import sys
import json
import argparse

try:
    from ffmpeg import FFmpeg, FFmpegError, Progress

    from rich.progress import TaskProgressColumn, TextColumn
    from rich.progress import BarColumn, TimeRemainingColumn
    from rich.progress import Progress as ProgressBar
    from rich.prompt import Prompt, IntPrompt, Confirm
    from rich.console import Console
    from rich import traceback
    
except ModuleNotFoundError as e:
    _error = str(e)
    print(f" [Fatal] {_error.capitalize()}")
    print(f" - Make sure you install all required modules by using `pip`")
    print(f" - Exiting...")
    raise SystemExit(-1)


if sys.platform == "darwin":
    DEFAULT_OPTIONS = {
        'r': '24',
        's': '1920x1080',
        'codec:v': 'h264_videotoolbox', 
        'crf': '21', 
        'codec:a': 'libmp3lame', 
        'ar': '48000', 
        'b:a': '320k', 
        'ac': '2'
    }
else:
    DEFAULT_OPTIONS = {
        'r': '24',
        's': '1920x1080',
        'codec:v': 'libx264', 
        'crf': '21', 
        'codec:a': 'libmp3lame', 
        'ar': '48000', 
        'b:a': '320k', 
        'ac': '2'
    }


class MetadataLogger():
    """The MetadataLogger() class's purpose is to log metadata (duh)"""
    
    @staticmethod
    def log_metadata(_metadata: dict) -> None:
        """Prints the contents of a metadata dictionary from ffprobe
        
        Returns:
            None; the function outputs the information of the different
            streams detected onto the console. 
        """
        _metadata = _metadata["streams"]
        Console().log(f"[Info] Retrieved source info: ", highlight = False)
        for _stream in _metadata:
            if _stream["codec_type"] == "video":
                MetadataLogger._log_video_metadata(_stream)
            elif _stream["codec_type"] == "audio":
                MetadataLogger._log_audio_metadata(_stream)
            else:
                Console().log(f"[bold]- Auxiliary (source stream {_stream["codec_type"]})")
        Console().log(f"[Info] End source info ", highlight = False)
        return
    
    @staticmethod
    def _log_video_metadata(_video_stream: dict) -> None:
        # Disregard this mess and be glad you didn't have to debug this
        try: _idx: str = f"{_video_stream['index']}"
        except: _idx: str = f"[yellow]-"
        try: _col: str = f"{_video_stream['color_space']}"
        except: _col: str = f"[yellow]-"
        try: _fmt: str = f"{_video_stream['codec_long_name']}"
        except: _fmt: str = f"[yellow]-"
        try: _res: str = f"{_video_stream['width']}x{_video_stream['height']}"
        except: _res: str = f"[yellow]-"
        try: _fps: str = f"{MetadataLogger._parse_framerate(_video_stream['avg_frame_rate'])}"
        except: _fps: str = f"[yellow]-"
        try: _dur: str = f"{round(float(_video_stream['duration']), 2)}"
        except: _dur: str = f"[yellow]-"
        try: _fra: str = f"{round(float(_fps) * float(_dur), 2)}"
        except: _fra: str = f"[yellow]-"
        
        Console().log(f"[bold]- Video (source stream {_idx})")
        Console().log(f"|    Video codec      : {_fmt}", highlight = False)
        Console().log(f"|    Video color      : {_col}", highlight = False)
        Console().log(f"|    Video resolution : {_res}", highlight = False)
        Console().log(f"|    Video framerate  : {_fps} fps", highlight = False)
        Console().log(f"|    Video length     : {_dur} seconds", highlight = False)
        Console().log(f"|    Total frames     : {_fra} frames", highlight = False)
        return
        
    @staticmethod
    def _log_audio_metadata(_audio_stream: dict) -> None:
        # Disregard this mess and be glad you didn't have to debug this
        try: _idx: str = f"{_audio_stream['index']}"
        except: _idx: str = f"[yellow]-"
        try: _fmt: str = f"{_audio_stream['codec_long_name']}"
        except: _fmt: str = f"[yellow]-"
        try: _prf: str = f"{_audio_stream['profile']}"
        except: _prf: str = f"[yellow]-"
        try: _smp: str = f"{_audio_stream['sample_rate']}"
        except: _smp: str = f"[yellow]-"
        try: _chn: str = f"{_audio_stream['channels']}"
        except: _chn: str = f"[yellow]-"
        try: _lay: str = f"{_audio_stream['channel_layout'].capitalize()}"
        except: _lay: str = f"[yellow]-"
        try: _btr: str = f"{int(_audio_stream['bit_rate']) // 1000}"
        except: _btr: str = f"[yellow]-"
        
        Console().log(f"[bold]- Audio (source stream {_idx})")
        Console().log(f"|    Audio codec      : {_fmt}", highlight = False)
        Console().log(f"|    Audio profile    : {_prf}", highlight = False)
        Console().log(f"|    Audio samplerate : {_smp} Hz", highlight = False)
        Console().log(f"|    Audio channels   : {_chn}", highlight = False)
        Console().log(f"|    Audio layout     : {_lay}", highlight = False)
        Console().log(f"|    Audio bitrate    : {_btr} kb/s", highlight = False)
        return
    
    @staticmethod
    def _parse_framerate(_fps: str) -> str:
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
        return str(round(_numerator / _denominator, 2))


class MediaManager():
    """The MediaManager() class represents a media file, its metadata, and the user's 
    options on its encoding options
    """

    def __init__(
        self, 
        input_path: str, 
        debug: bool = False
    ) -> None:
        """Initializes an instance of `MediaManager`

        Args:
            inputPath - the path of the media file that the object 
            will represent
        """
        self.console = Console(highlight = False)
        self.error_console = Console(stderr = True, style = "bold red")

        self.input_path = input_path
        self.get_metadata(debug)
        
        return

    def get_metadata(
        self, 
        _debug: bool = False
    ) -> None:
        """Gets the metadata of the media file that the object is
        currently representing. Also loads the audio/video streams

        Returns:
            None - instead, fetches the metadata into the class attribute 
            `self.metadata`
        """
        self.console.log("[Info] Probing file properties and metadata with ffprobe...")
        _ffprobe = FFmpeg(executable = "ffprobe").input(
                self.input_path,
                print_format = 'json',
                show_streams = None
        )

        @_ffprobe.on("stderr")
        def ffmpeg_out(_Msg: str) -> None:
            if _debug:
                self.console.log(f"[FFprobe] {_Msg}")

        self.metadata: dict = json.loads(_ffprobe.execute())
        
        self.audio_stream = self.get_audio_stream()
        self.video_stream = self.get_video_stream()
        return

    def ask_encode_options(
        self, 
        _default: bool = False
    ) -> None:
        """Asks the user for encoding options
        
        Note: Tries to conform to the user's request as much as possible, 
            however in the event that an audio/video stream cannot be 
            discovered, the ask...() function automatically aborts. 
            
            This may lead to unexpected issues. 
        
        Args:
            _default - whether to use the default options
            
        Returns: 
            None - instead, fetches options from the user and stores it inside
            the class attribute `self.options`. 
        """
        if _default:
            self.options = DEFAULT_OPTIONS
            return

        self.console.print()
        self.console.print("[bold] -*- Encoding options -*-")
        self.console.print()
        self.console.print("Encode for...")
        self.console.print("[1] Audio only")
        self.console.print("[2] Video only")
        self.console.print("[3] Both (default)")
        _encode = Prompt.ask(
            "Select an option", 
            choices = ["1", "2", "3"], 
            default = "3"
        )

        self.options: dict = {}
        if _encode == "1": 
            self.options = self.ask_audio_options()
            self.options["vn"] = None
        if _encode == "2": 
            self.options = self.ask_video_options()
            self.options["an"] = None
        if _encode == "3": 
            self.options = self.ask_audio_options() | self.ask_video_options()
            
        self.console.print()
        _metadata_preserve = Prompt.ask(
            "Enable file metadata preserving",
            choices = ["y", "n"],
            default = "y"
        )
        
        if _metadata_preserve:
            self.options["movflags"] = "use_metadata_tags"

        self.console.print()
        self.console.log(f"[Log] Finished asking encoding options")
        return

    def ask_audio_options(self) -> dict:
        """Asks the user for audio encoding options

        Returns: 
            A dictionary containing the arguments to pass to FFmpeg. If no 
            audio streams are discovered, returns an empty dictionary
        """

        if self.audio_stream == -1:
            self.error_console.log("[Error] No audio stream detected in metadata! ")
            self.error_console.log("- This may lead to unexpected issues")
            self.error_console.log("- Skipping audio encoding...")
            return {}
        
        _ret: dict = {}
        self.console.print()
        self.console.print("[bold] -*- Audio options -*-")
        self.console.print()
        self.console.print("Audio codec presets -")
        self.console.print("[1] AAC")
        self.console.print("[2] MP3 (default)")
        self.console.print("[3] ALAC")
        self.console.print("[4] FLAC")
        self.console.print("[5] Custom encoder")
        _codec = Prompt.ask(
            "Select a codec", 
            choices = ["1", "2", "3", "4", "5"],
            default = "2"
        )

        _codec = self._parse_codec_audio(_codec)

        self.console.print()
        self.console.print("Audio samplerate presets -")
        self.console.print("[1] 16000hz")
        self.console.print("[2] 44100hz")
        self.console.print("[3] 48000hz (default)")
        self.console.print("[4] 96000hz")
        self.console.print("[5] Custom samplerate")
        _samplerate = Prompt.ask(
            "Select a samplerate", 
            choices = ["1", "2", "3", "4", "5"], 
            default = "3"
        )

        _samplerate = self._parse_samplerate(_samplerate)
        
        self.console.print()
        self.console.print("Audio bitrate presets -")
        self.console.print("[1] 96k")
        self.console.print("[2] 128k")
        self.console.print("[3] 192k (default)")
        self.console.print("[4] 320k")
        self.console.print("[5] Custom bitrate")
        _bitrate = Prompt.ask(
            "Select a bitrate", 
            choices = ["1", "2", "3", "4", "5"], 
            default = "3"
        )

        _bitrate = self._parse_bitrate(_bitrate)
        
        _channels: int = self.metadata["streams"][self.audio_stream]["channels"]
        
        _ret["codec:a"] = _codec
        _ret["ar"] = _samplerate
        _ret["b:a"] = _bitrate
        _ret["ac"] = str(_channels)

        return _ret

    def ask_video_options(self) -> dict:
        """Asks the user for video encoding options

        Returns: 
            A dictionary containing the arguments to pass to FFmpeg
        """
        
        if self.video_stream == -1:
            self.error_console.log("[Error] No video stream detected in metadata! ")
            self.error_console.log("- This may lead to unexpected issues")
            self.error_console.log("- Skipping video encoding...")
            return {}
            
        _ret: dict = {}
        self.console.print()
        self.console.print("[bold]-*- Video options -*-")

        self.console.print()
        self.console.print("Video resolution presets -")
        self.console.print("[1] 1280x720")
        self.console.print("[2] 1920x1080 (default)")
        self.console.print("[3] 2560x1440")
        self.console.print("[4] 3840x2160")
        self.console.print("[5] Custom resolution")
        _resolution = Prompt.ask(
            "Select a resolution", 
            choices = ["1", "2", "3", "4", "5"], 
            default = "2"
        )

        _resolution = self._parse_resolution(_resolution)

        self.console.print()
        self.console.print(f"Video framerate presets -")
        self.console.print(f"[1] 24fps (default)")
        self.console.print(f"[2] 30fps")
        self.console.print(f"[3] 50fps")
        self.console.print(f"[4] 60fps")
        self.console.print(f"[5] Custom framerate")
        _framerate = Prompt.ask(
            "Select a framerate", 
            choices = ["1", "2", "3", "4", "5"], 
            default = "1"
        )

        _framerate = self._parse_framerate(_framerate)

        self.console.print()
        self.console.print(f"Video codec presets -")
        self.console.print(f"[1] H.264", highlight = False)
        self.console.print(f"[2] H.265 (default)", highlight = False)
        self.console.print(f"[3] AV1")
        self.console.print(f"[4] VP9")
        self.console.print(f"[5] Custom codec")
        _codec = Prompt.ask(
            "Select a codec", 
            choices = ["1", "2", "3", "4", "5"], 
            default = "2"
        )

        _codec = self._parse_codec_video(_codec)

        self.console.print()
        self.console.print(f"Video quality -")
        _doLossless = Confirm.ask("Enable lossless video (CRF = 0)")


        _ret["r"] = _framerate
        _ret["s"] = _resolution
        _ret["codec:v"] = _codec

        if _doLossless:
            _ret["crf"] = "0"
        else:
            _ret["crf"] = IntPrompt.ask("Enter a CRF value (0-51)")

        return _ret
        
    def get_audio_stream(self) -> int:
        """Gets the index of the first audio stream in self.metadata. If
        multiple streams are present, the first stream is returned, and
        the rest of the streams are ignored
        
        Returns:
            An integer representing the channel of the first audio
            stream. If no audio streams are present in the metadata,
            the function returns -1. 
        """
        _ret: int = -1
        for _stream in self.metadata["streams"]:
            if _stream["codec_type"] == "audio":
                self.console.log(f"[Info] First audio stream found (stream {_stream["index"]})")
                _ret = _stream["index"]
                break
        
        return _ret
        
    def get_video_stream(self) -> int:
        """Gets the index of the first video stream in self.metadata. If
        multiple streams are present, the first stream is returned, and
        the rest of the streams are ignored
        
        Returns:
            An integer representing the channel of the first video
            stream. If no audio streams are present in the metadata,
            the function returns -1. 
        """
        _ret: int = -1
        for _stream in self.metadata["streams"]:
            if _stream["codec_type"] == "video":
                self.console.log(f"[Info] First video stream found (stream {_stream["index"]})")
                _ret = _stream["index"]
                break
        
        return _ret

    def get_total_secs(self) -> int:
        """Gets the total length (in seconds) of the first video stream

        Returns:
            An integer representing the length (in seconds)
        """
        _ret = self.metadata["streams"][self.video_stream]["duration"]
        _ret = float(_ret)
        return int(_ret)

    def get_framerate(self) -> int:
        """Gets the average framerate of the first video stream

        Returns:
            An integer representing the framerate
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

    @staticmethod
    def _parse_resolution(_resolution: str) -> str:
        if _resolution == "1": 
            return "1280x720"
        if _resolution == "2": 
            return "1920x1080"
        if _resolution == "3": 
            return "2560x1440"
        if _resolution == "4": 
            return "3840x2160"
        if _resolution == "5": 
            return Prompt.ask("Enter custom resolution (e.g. 2160x1440)")
        return "1920x1080"

    @staticmethod
    def _parse_codec_video(_codec: str) -> str:
        if _codec == "1": 
            if sys.platform == "darwin": return "h264_videotoolbox"
            else: return "libx264"
        if _codec == "2": 
            if sys.platform == "darwin": return "hevc_videotoolbox"
            else: return "libx265"
        if _codec == "3": 
            return "libsvtav1"
        if _codec == "4": 
            return "libvpx-vp9"
        if _codec == "5": 
            return Prompt.ask("Enter custom video encoder (e.g. libwebp)")
        return "libx264"

    @staticmethod
    def _parse_codec_audio(_codec: str) -> str:
        if _codec == "1": 
            return "aac"
        if _codec == "2": 
            return "libmp3lame"
        if _codec == "3": 
            return "alac"
        if _codec == "4": 
            return "flac"
        if _codec == "5": 
            return Prompt.ask("Enter custom audio encoder (e.g. libtwolame)")
        return "libx264"

    @staticmethod
    def _parse_framerate(_framerate: str) -> str:
        if _framerate == "1": 
            return "24"
        if _framerate == "2": 
            return "30"
        if _framerate == "3": 
            return "50"
        if _framerate == "4": 
            return "60"
        if _framerate == "5": 
            return Prompt.ask("Enter custom framerate (e.g. 23.976)")
        return "24"

    @staticmethod
    def _parse_samplerate(_samplerate: str) -> str:
        if _samplerate == "1": 
            return "16000"
        if _samplerate == "2": 
            return "44100"
        if _samplerate == "3": 
            return "48000"
        if _samplerate == "4": 
            return "96000"
        if _samplerate == "5": 
            return Prompt.ask("Enter custom samplerate (e.g. 22050)")
        return "48000"

    @staticmethod
    def _parse_bitrate(_bitrate: str) -> str:
        if _bitrate == "1": 
            return "96k"
        if _bitrate == "2": 
            return "128k"
        if _bitrate == "3": 
            return "192k"
        if _bitrate == "4": 
            return "320k"
        if _bitrate == "5": 
            return Prompt.ask("Enter custom bitrate (e.g. 160)")
        return "192k"


class Program():
    """
    a media file converter using the ffmpeg engine. 
    """

    def __init__(self) -> None:
        """Initializes an instance of `Program`"""
        self.console = Console(highlight = False)
        self.error_console = Console(stderr = True, style = "bold red")
        self.debug = False
        self.default = False

        try: 
            self.parse_args()
        except Exception as e: 
            _error = str(e)
            self.error_console.log(f"[Error] Program().parse_args() failed: {_error}")
            self.error_console.log()
        
        self.check_ffmpeg()

        if self.debug: 
            self.console.log(f"[yellow][Warning] Using debug mode")
        if self.default: 
            self.console.log(f"[yellow][Warning] Using all default options")
            
        self.console.log("[Info] Initialized an instance of mpeg-convert")
        return

    def parse_args(self) -> None:
        """Parses the command-line arguments from the user
        
        Notes:
            Commands can be listed with the option `-h` or
            `--help`. 
        """
        _parser = argparse.ArgumentParser(
            description = self.__doc__,
            usage = "mpeg-convert [options] <file.in> <file.out>",
            argument_default = argparse.SUPPRESS
        )

        _parser.add_argument(
            "input", 
            type = str, 
            help = "the input file to convert from"
        )

        _parser.add_argument(
            "output", 
            type = str, 
            help = "the output file to convert to"
        )

        _parser.add_argument(
            "-d", "--debug", 
            action = "store_true", 
            default = False,
            help = "outputs all ffmpeg logs to the console"
        )

        _parser.add_argument(
            "--default", 
            action = "store_true", 
            default = False,
            help = "use all default settings for encoding"
        )

        _args = _parser.parse_args()

        self.input = _args.input
        self.output = _args.output
        self.debug = _args.debug
        self.default = _args.default

        _cwd = os.getcwd()
        _cwd = _cwd + "/"
        if self.input[0] != "/" and self.input[0] != "~":
                self.input = _cwd + self.input
        if self.output[0] != "/" and self.output[0] != "~":
            self.output = _cwd + self.output
        return

    def check_ffmpeg(self):
        """Checks whether FFmpeg is installed and on the system path"""
        try:
            _ffprobe = FFmpeg(executable = "ffprobe").option("h")
            _ffmpeg = FFmpeg(executable = "ffmpeg").option("h")
            _ffprobe.execute()
            _ffmpeg.execute()
        except FileNotFoundError:
            self.error_console.log(
                "[Fatal] Program().check_ffmpeg() failed: could not find FFmpeg installation in path",
                "- Make sure FFmpeg is installed and is in path before launching this script"
            )

            raise SystemExit(127)
        return

    def process(self) -> None:
        """Processes the input file by instantiating a MediaManager() object"""
        self.media = MediaManager(self.input, self.debug)
        self.framerate   = None
        self.total_secs  = None
        self.total_frame = None
        try:
            self.framerate   = self.media.get_framerate()
            self.total_secs  = self.media.get_total_secs()
            self.total_frame = self.total_secs * self.framerate
        except Exception:
            self.error_console.log(f"[yellow][Warning] Failed retrieving total frames")
            self.error_console.log(f"[yellow]- The program uses the total frames in the video to calculate remaining time")
            self.error_console.log(f"[yellow]- Perhaps you are converting an audio file?")
            self.error_console.log(f"[yellow]- The progress bar will be indeterminate")
        
        try:
            MetadataLogger.log_metadata(self.media.metadata)
        except Exception as e:
            _error = str(e)
            self.error_console.log(f"[Error] MetadataLogger().log_metadata() failed: {_error}")

        # MPEG-Convert has only been tested for a max
        # of 3 streams (video, audio, subtitles)
        if len(self.media.metadata['streams']) > 3:
            self.console.log()
            self.console.log(f"[yellow][Warning] Multiple video/audio streams detected")
            self.console.log(f"- Mpeg-convert has not been tested for multiple video/audio streams")
            self.console.log(f"- You are entering unknown territory if you proceed! ")
            self.console.log(f"- This could also be a false detection")

        self.media.ask_encode_options(self.default)
        return

    def convert(self) -> None:
        """Starts the conversion of the media file"""

        self.instance = (FFmpeg()
            .option("y")
            .input(self.input)
            .output(
                self.output,
                self.media.options
            ))

        self.last_frame: int = 0

        with ProgressBar(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(text_format = "[progress.percentage]{task.percentage:>0.1f}% ({task.completed}/{task.total} frames)"),
            TimeRemainingColumn(elapsed_when_finished = True),
            console = self.console
        ) as _bar:

            @self.instance.on("progress")
            def update_prog(_progress: Progress) -> None:
                _bar.update(_task, total = self.total_frame)
                _bar.update(_task, advance = _progress.frame - self.last_frame)
                self.last_frame = _progress.frame

            @self.instance.on("start")
            def show_args(_args: list[str]):
                self.console.log(f"[Info] Initiated FFmpeg task with the following command: {_args}")

            @self.instance.on("stderr")
            def ffmpeg_out(_Msg: str) -> None:
                if self.debug:
                    self.console.log(f"[FFmpeg] {_Msg}")

            _task = _bar.add_task("[green]Transcoding file...", total = None)
            self.instance.execute()
        return

    def run(self) -> None:
        """The entrypoint of the program"""
        
        self.console.log(f"[Info] Received (parsed) command-line arguments: '{self.input}' and '{self.output}'")

        try:
            self.process()
            self.convert()
        except FFmpegError as _error:
            _ffmpeg_args = ""
            for _arg in _error.arguments:
                _ffmpeg_args = _ffmpeg_args + _arg + " "

            self.error_console.log(f"[Fatal] An ffmpeg exception has occured!")
            self.error_console.log(f"[red]- Error message from ffmpeg: [white]{_error.message.lower()}", highlight = False)
            self.error_console.log(f"[red]- Arguments to execute ffmpeg: [white]{_ffmpeg_args.lower()}", highlight = False)
            self.error_console.log(f"- Use the `--debug` option to hear ffmpeg output", highlight = False)
            self.error_console.log()
            self.error_console.log(f"- Common pitfalls: ", highlight = False)
            self.error_console.log(f"  * Does the output file have an extension?", highlight = False)
            self.error_console.log(f"  * Does the extension match the codec?", highlight = False)
            self.error_console.log(f"  * Is the encoder installed on your system?", highlight = False)
            self.error_console.log(f"[Info] Exiting mpeg-convert...")
            raise SystemExit(1)

        self.console.log(f"[green][Info] Succesfully executed mpeg-convert")
        self.console.log(f"[Info] Safely exiting mpeg-convert...")
        return


if __name__ == "__main__":
    try:
        traceback.install(show_locals = True)
        instance = Program()
        instance.run()
        raise SystemExit(0)
    except KeyboardInterrupt:
        Console().print()
        Console().log("[yellow][Warning] Program received KeyboardInterrupt...")
        Console().log("[yellow][Warning] Force quitting with os._exit()...")
        os._exit(0)   # Force terminate all threads
