#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file uses the following styles for token names: 
#     PascalCase       Class name
#     camelCase        Variable or function/method name
#     _underscore      Variable/function should be used only in the scope
#                      it's declared in (and should not be modified by user)
#
# This file uses 4 spaces for indentation

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
    _errormsg = str(e)
    print(f" [Fatal] {_errormsg.capitalize()}")
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


class MediaManager():

    def __init__(self, inputPath: str, debug = False) -> None:
        """Initializes an instane of `MediaManager`

        Args:
            inputPath - the path of the media file that the object 
            will represent
        """
        self.console = Console(highlight = False)

        self.inputPath = inputPath
        self.getMetadata(debug)

    def getMetadata(self, _debug = False) -> None:
        """Gets the metadata of the media file that the object is
           currently representing

        Returns:
            None - instead, fetches the metadata into the class attribute 
            `self.metadata`
        """
        self.console.log("[Info] Probing file properties and metadata...")
        _ffprobe = FFmpeg(executable = "ffprobe").input(
                self.inputPath,
                print_format = 'json',
                show_streams = None
        )

        @_ffprobe.on("stderr")
        def ffmpegOutput(_Msg: str) -> None:
            if _debug:
                self.console.log(f"[FFprobe] {_Msg}")

        self.metadata: dict = json.loads(_ffprobe.execute())
        return

    def askEncodeOptions(self, _default: bool = False) -> None:
        """Asks the user for encoding options
        
        Args:
            _default - whether to use the default options
        Returns: 
            None - instead, fetches options from the user and stores it inside
            the class attribute `self.options`
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
            self.options = self.askAudioOptions()
            self.options["vn"] = None
        if _encode == "2": 
            self.options = self.askVideoOptions()
            self.options["an"] = None
        if _encode == "3": 
            self.options = self.askVideoOptions() | self.askAudioOptions()

        self.console.log(f"[Debug] Finished asking encoding options")
        return

    def askAudioOptions(self) -> dict:
        """Asks the user for audio encoding options

        Returns: 
            A dictionary containing the arguments to pass to FFmpeg
        """
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

        _codec = self._parseCodecAudio(_codec)

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

        _samplerate = self._parseSamplerate(_samplerate)
        
        self.console.print()
        self.console.print("Audio bitrate presets -")
        self.console.print("[1] 96k")
        self.console.print("[2] 128k")
        self.console.print("[3] 192k (default)")
        self.console.print("[4] 320k")
        self.console.print("[5] Custom bitrate")
        _bitrate = Prompt.ask(
            "Select a birate", 
            choices = ["1", "2", "3", "4", "5"], 
            default = "3"
        )

        _bitrate = self._parseBitrate(_bitrate)

        _channels = self.metadata["streams"][1]["channels"]

        _ret["codec:a"] = _codec
        _ret["ar"] = _samplerate
        _ret["b:a"] = _bitrate
        _ret["ac"] = str(_channels)

        return _ret

    def askVideoOptions(self) -> dict:
        """Asks the user for video encoding options

        Note:
            The CRF value is hard-coded

        Returns: 
            A dictionary containing the arguments to pass to FFmpeg
        """
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

        _resolution = self._parseResolution(_resolution)

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

        _framerate = self._parseFramerate(_framerate)

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

        _codec = self._parseCodecVideo(_codec)

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

    def getTotalSecs(self) -> int:
        """Gets the total length (in seconds) of the current video file

        Note: 
            Assumes that `stream 0` is the one and only video stream in the 
            media file

        Returns:
            An integer representing the length (in seconds) of the current 
            video file
        """
        _ret = self.metadata["streams"][0]["duration"]
        _ret = float(_ret)
        return int(_ret)

    def getFramerate(self) -> int:
        """Gets the average framerate of the current video file

        Note: 
            Assumes that `stream 0` is the one and only video stream in 
            the media file

        Returns:
            An integer representing the framerate of the current video file
        """
        _ret = self.metadata["streams"][0]["avg_frame_rate"]
        _ret = _ret[:-2]
        return int(_ret)

    @staticmethod
    def _parseResolution(_resolution: str) -> str:
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
    def _parseCodecVideo(_codec: str) -> str:
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
    def _parseCodecAudio(_codec: str) -> str:
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
    def _parseFramerate(_framerate: str) -> str:
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
    def _parseSamplerate(_samplerate: str) -> str:
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
    def _parseBitrate(_bitrate: str) -> str:
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
        self.errorConsole = Console(stderr = True, style = "bold red")
        self.debug = False
        self.default = False

        try: 
            self.parseArgs()
        except Exception as e: 
            _errormsg = str(e)
            self.errorConsole.log(f"[Fatal] Program().parseArgs() failed: {_errormsg}")
            self.errorConsole

        self.checkFFmpeg()

        if self.debug: 
            self.console.log(f"[yellow][Warning] Using debug mode")
        if self.default: 
            self.console.log(f"[yellow][Warning] Using all default options")

    def parseArgs(self) -> None:
        """Parses the command-line arguments from the user"""
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
            help = "outputs all FFmpeg logs to the console"
        )

        _parser.add_argument(
            "--default", 
            action = "store_true", 
            default = False,
            help = "use default settings for encoding"
        )

        _args = _parser.parse_args()

        self.input = _args.input
        self.output = _args.output
        self.debug = _args.debug
        self.default = _args.default

        _cwd = os.getcwd()
        if self.input[0] != "/" and self.input[0] != "~":
                self.input = _cwd + "/" + self.input
        if self.output[0] != "/" and self.output[0] != "~":
            self.output = _cwd + "/" + self.output

    @staticmethod
    def checkDebug(_argc: int, _argv: list[str]) -> tuple:
        for i in range(_argc):
            if _argv[i] == "-d" or _argv[i] == "--debug":
                return (True, i)
        return (False, -1)

    def checkFFmpeg(self):
        """Checks whether FFmpeg is installed and on the system path"""
        try:
            _ffprobe = FFmpeg(executable = "ffprobe").option("h")
            _ffmpeg = FFmpeg().option("h")
            _ffprobe.execute()
            _ffmpeg.execute()
        except FileNotFoundError:
            self.errorConsole.log(
                "[Fatal] Program().checkFFmpeg() failed: could not find FFmpeg in path\n\
                - Make sure FFmpeg is installed and is in path before launching this script"
            )

            raise SystemExit(127)

    def logMetadata(self):
        """Prints the metadata of a media (MediaManager class) file"""
        _metadata = self.media.metadata
        _videoData = _metadata['streams'][0]
        _audioData = _metadata['streams'][1]
        self.console.log(f"[Info] Detected source info: ")
        self.console.log(f"[bold]- Video (source stream 0)")
        self.console.log(f"|    Video codec      : {_videoData['codec_long_name']}")
        self.console.log(f"|    Video color      : {_videoData['color_space']}")
        self.console.log(f"|    Video resolution : {_videoData['width']}x{_videoData['height']}")
        self.console.log(f"|    Video framerate  : {self.framerate} fps")
        self.console.log(f"|    Video length     : {self.totalSecs} seconds")
        self.console.log(f"|    Total frames     : {self.totalFrame} frames")
        self.console.log(f"[bold]- Audio (source stream 1)")
        self.console.log(f"|    Audio codec      : {_audioData['codec_long_name']}")
        self.console.log(f"|    Audio profile    : {_audioData['profile']}")
        self.console.log(f"|    Audio samplerate : {_audioData['sample_rate']} Hz")
        self.console.log(f"|    Audio channels   : {_audioData['channels']}")
        self.console.log(f"|    Audio layout     : {_audioData['channel_layout'].capitalize()}")
        self.console.log(f"|    Audio bitrate    : {int(_audioData['bit_rate']) // 1000} kb/s")

    def process(self) -> None:
        """Processes the input file by instantiating a MediaManager() object"""
        self.media = MediaManager(self.input, self.debug)
        self.framerate: int  = self.media.getFramerate()
        self.totalSecs: int  = self.media.getTotalSecs()
        self.totalFrame: int = self.totalSecs * self.framerate
        try:
            self.logMetadata()
        except Exception as e:
            _errormsg = str(e)
            self.errorConsole.log(f"[Fatal] Program().logMetadata() failed: {_errormsg}")
            self.errorConsole

        if len(self.media.metadata['streams']) > 3:
            self.console.log()
            self.console.log(f"[red][Warning] Multiple video/audio streams detected")
            self.console.log(f"- Mpeg-compress has not been tested for multiple video/audio streams")
            self.console.log(f"- You are entering unknown territory if you proceed! ")
            self.console.log(f"- This could also be a false detection")

        self.media.askEncodeOptions(self.default)

    def convert(self) -> None:
        """Starts the conversion of the media file"""

        self.ffmpegInstance = (FFmpeg()
            .option("y")
            .input(self.input)
            .output(
                self.output,
                self.media.options
            ))

        self.lastFrame: int = 0

        with ProgressBar(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(text_format = "[progress.percentage]{task.percentage:>0.1f}% ({task.completed}/{task.total} frames)"),
            TimeRemainingColumn(elapsed_when_finished = True),
            console = self.console
        ) as _bar:

            @self.ffmpegInstance.on("progress")
            def updateProgress(_progress: Progress) -> None:
                _bar.update(_task, total = self.totalFrame)
                _bar.update(_task, advance = _progress.frame - self.lastFrame)
                self.lastFrame = _progress.frame

            @self.ffmpegInstance.on("start")
            def showArgs(_args: list[str]):
                self.console.log(f"[Info] Initiated FFmpeg task with the following command: {_args}")

            @self.ffmpegInstance.on("stderr")
            def ffmpegOutput(_Msg: str) -> None:
                if self.debug:
                    self.console.log(f"[FFmpeg] {_Msg}")

            _task = _bar.add_task("[green]Transcoding file...", total = None)
            self.ffmpegInstance.execute()

    def run(self) -> None:
        """The entrypoint of the program"""

        self.parseArgs()
        self.console.log(f"[Info] Parsed command-line arguments: '{self.input}' and '{self.output}'")

        try:
            self.process()
            self.convert()
        except FFmpegError as _error:
            _ffmpegArgs = ""
            for _arg in _error.arguments:
                _ffmpegArgs = _ffmpegArgs + _arg + " "

            self.errorConsole.log(f"[Fatal] An FFmpeg exception has occured!")
            self.errorConsole.log(f"- Error message from FFmpeg: {_error.message.lower()}")
            self.errorConsole.log(f"- Arguments to execute FFmpeg: {_ffmpegArgs.lower()}")
            self.errorConsole.log(f"[Info] Exiting mpeg-convert...")
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
        Console().log("[Warning] Program received KeyboardInterrupt...")
        Console().log("[Warning] Force quitting with os._exit()...")
        os._exit(0)   # Force terminate all threads
