"""High level logic and control flow of the program"""

import sys
import time

from mpeg_convert import utils
from mpeg_convert import options
from mpeg_convert import metadata
from mpeg_convert import argparsing

from ffmpeg import FFmpeg, FFmpegError, Progress

from rich.progress import TaskProgressColumn, TextColumn
from rich.progress import BarColumn, TimeRemainingColumn
from rich.progress import Progress as ProgressBar
from rich.console import Console

from mpeg_convert.metadata import MetadataLogger


class Program:
    """A media file converter using the ffmpeg engine"""

    def __init__(self) -> None:
        """Initializes an instance of `Program` by initializing the console, 
        parsing the command-line arguments, and verifying that the installation
        of ffmpeg is discoverable
        """

        self.console = Console(highlight=False)
        self.error_console = Console(style="red", highlight=False)

        self.verbose = False
        self.default = False

        if not sys.stdout.isatty():
            self.console.log("[yellow][Warning] Mpeg-convert is not outputting to a tty")
            self.console.log("[yellow]- You might be piping the output for debugging")
            self.console.log("[yellow]- Some functionalities will be limited")

        try:
            _parsed_args = argparsing.parse_args()
            self.input = _parsed_args["input"]
            self.output = _parsed_args["output"]
            self.verbose = _parsed_args["verbose"]
            self.default = _parsed_args["default"]
        except Exception as e:
            _error = str(e)
            raise utils.FatalError(
                1,
                f"Program.parse_args() failed: {_error}",
                f"- Mpeg-convert usage: mpeg-convert \\[options] <file.in> <file.out>",
                f"- MPEG-convert terminating due to inapt command-line arguments"
            )

        self.check_ffmpeg()

        self.instance = None
        self.framerate = None
        self.start_time = None
        self.last_frame = None

        self.media = None
        self.options = None
        self.options_handler = None

        self.total_secs = None
        self.total_frame = None
        return

    def check_ffmpeg(self):
        """Checks whether FFmpeg is installed and on the system path
        
        If FFmpeg is not discoverable, function raises SystemExit and terminated
        program. Otherwise, the function executes successfully
        """
        try:
            self.console.log("[Info] Verifying FFmpeg installation")
            _ffprobe = FFmpeg(executable="ffprobe").option("h")
            _ffmpeg = FFmpeg(executable="ffmpeg").option("h")
            _ffprobe.execute()
            _ffmpeg.execute()
        except FileNotFoundError:
            raise utils.FatalError(
                127,
                "Could not detect FFmpeg executable in system path",
                " - Make sure FFmpeg is installed",
                " - Make sure FFmpeg is in $PATH"
            )

        return

    def process(self) -> None:
        """Processes the input file for metadata information (such as 
        framerate, length, etc.), outputs the metadata onto the console,
        and asks the user options on how the program (ffmpeg) should 
        transcode the input file
        
        Because the program uses the total number of video frames to
        determine the progress, audio files (which have no video frames)
        will cause the program's progress bar to be indeterminate
        """
        self.media = metadata.MetadataManager(self.input, self.verbose)
        self.framerate = None
        self.total_secs = None
        self.total_frame = None

        try:
            self.framerate = self.media.get_framerate()
            self.total_secs = self.media.get_total_secs()
            self.total_frame = self.total_secs * self.framerate
        except ZeroDivisionError:
            self.error_console.log(f"[yellow][Warning] Failed retrieving total frames")
            self.error_console.log(f"[yellow] - Mpeg-convert uses video frames to calculate remaining time")
            self.error_console.log(f"[yellow] - The progress bar will be indeterminate")
            self.error_console.log(f"[yellow] - Perhaps you are converting an audio file?")

        # MPEG-Convert has only been tested for a max
        # of 3 streams (video, audio, subtitles)
        if len(self.media.metadata['streams']) > 3:
            self.console.log(f"[yellow][Warning] Multiple video/audio streams detected")
            self.console.log(f" - Mpeg-convert has not been tested for multiple video/audio streams")
            self.console.log(f" - You are entering unknown territory if you proceed! ")
            self.console.log(f" - This could also be a false detection")

        MetadataLogger.log_metadata(self.media.metadata)

        self.options_handler = options.OptionsHandler(
            self.media.metadata,
            self.media.audio_stream,
            self.media.video_stream,
            self.output
        )

        self.options = self.options_handler.ask_encode_options(self.default)
        self.console.log(f"[Info] Finished gathering encoding options")
        return

    def convert(self) -> None:
        """Starts the conversion of the media file using the FFmpeg() 
        class from python-ffmpeg. Uses the options and metadata gathered 
        from Program::process() to display progress and pass other
        relevant information and arguments to the ffmpeg engine
        """
        self.instance = (
            FFmpeg()
            .option(self.options_handler.replace)
            .input(self.input)
            .output(
                self.output,
                self.options
            )
        )

        self.last_frame: int = 0
        self.start_time: float = time.time()

        with ProgressBar(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(
                    text_format="[progress.percentage]{task.percentage:>0.1f}% ({task.completed}/{task.total} frames)"),
                TextColumn("eta", style="cyan"),
                TimeRemainingColumn(elapsed_when_finished=True),
                console=self.console,
                transient=True
        ) as _bar:
            @self.instance.on("progress")
            def show_prog(_progress: Progress) -> None:
                _bar.update(_task, total=self.total_frame)
                _bar.update(_task, advance=_progress.frame - self.last_frame)
                self.last_frame = _progress.frame

            @self.instance.on("start")
            def show_args(_args: list[str]):
                self.console.log(f"[Info] Initiated FFmpeg task with the following command: {_args}")

            @self.instance.on("stderr")
            def show_cout(_msg: str) -> None:
                if self.verbose:
                    self.console.log(f"[FFmpeg] {_msg}")

            _task = _bar.add_task("[green]Transcoding file...", total=None)
            self.instance.execute()

        return

    def run(self) -> None:
        """The entrypoint of the program. Starts the processing and
        conversions, catches errors should they arise.
        """

        try:
            self.process()
            self.convert()
        except FFmpegError as _error:
            raise utils.FatalError(
                1,
                "An FFmpeg exception has occurred",
                f" - Error message from FFmpeg: '{_error.message}'",
                f" - Arguments to execute FFmpeg: {_error.arguments}",
                f" - Use the '-v' or '--verbose' option to hear FFmpeg output",
                f" - Common pitfalls: ",
                f"   * Does the output file have an extension?",
                f"   * Does the extension match the codec?",
                f"   * Is the encoder installed on your system?"
            )

        _total_time = round(time.time() - self.start_time, 2)
        _total_space = utils.readable_size(self.output)

        self.console.log(f"[green][Info] Successfully executed mpeg-convert")
        self.console.log(f"- Took {_total_time} seconds")
        self.console.log(f"- Took {_total_space} of space")
        self.console.log(f"- Output file saved to '{self.output}'")
        return
