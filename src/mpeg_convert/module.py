import os
import time
import json

from typing import List, Dict, Any, Union

from .utils import NamedPreset, UnnamedPreset, console, MODULE_PATH
from .utils import readable_size, load_config, expand_paths, open_file
from .utils import __version__, get_platform_version, get_python_version
from .exceptions import ForceExit

from rich.progress import TaskProgressColumn, TextColumn
from rich.progress import BarColumn, TimeRemainingColumn
from rich.progress import Progress as ProgressBar

from ffmpeg import FFmpeg, FFmpegError, Progress


def help() -> None:
    """Prints the help message from assets/help.txt"""
    with open(MODULE_PATH + "assets/help.txt") as f:
        print(f.read())


def version() -> None:
    """Prints the version information to the console"""
    _prgram_version = __version__.lower()
    _python_version = get_python_version().lower()
    _system_version = get_platform_version().lower()

    console.print(f" • program  : {_prgram_version}")
    console.print(f" • python   : {_python_version}")
    console.print(f" • platform : {_system_version}")
    console.print(f" • made with ♡ by zichen")


def config() -> None:
    """Opens the configuration file in the default editor. The configuration
    file is used to store presets (both named and unnamed), which is used
    when converting. See the readme file for more details on the config file
    """
    open_file(expand_paths("~/.local/share/mpeg-convert/config.yml"))
    return


class Metadata:
    """The MetadataManager() class represents a media's metadata"""

    def __init__(
        self,
        input_path: str,
    ) -> None:
        """Initializes an instance of `MediaManager`"""
        self.video_stream = None
        self.metadata = {}

        self.input_path = input_path
        self.get_metadata()
        return

    def get_metadata(
        self,
    ) -> None:
        """Gets the metadata of the media file that the object is
        currently representing. This method also loads the audio_stream
        and video_stream attributes, which represents the first
        video/audio stream the program encounters
        """
        ffprobe_instance = FFmpeg(executable="ffprobe").input(
            self.input_path,
            print_format='json',
            show_streams=None
        )

        self.metadata: dict = json.loads(ffprobe_instance.execute())
        self.video_stream = self.get_video_stream()
        return

    def get_video_stream(self) -> int:
        """Gets the index of the first video stream in self.metadata. If
        multiple streams are present, the first stream is returned, and
        the rest of the streams are ignored
        
        If no video streams are present in the metadata, the function 
        returns -1. 
        """
        ret: int = -1
        for stream in self.metadata["streams"]:
            if stream["codec_type"] == "video":
                ret = stream["index"]
                break
        return ret

    def get_total_secs(self) -> int:
        """Gets the total length (in seconds) of the first video stream"""
        ret = self.metadata["streams"][self.video_stream]["duration"]
        ret = float(ret)
        return int(ret)

    def get_framerate(self) -> int:
        """Gets the average framerate of the first video stream. Because
        the framerate is stored as a fraction in ffprobe, and some
        framerate are not whole numbers, this method has to manually parse
        the framerate by doing division in order to get the framerate as a
        floating-point integer
        """
        fps: str = self.metadata["streams"][self.video_stream]["avg_frame_rate"]

        numerator = ""
        for _ in range(len(fps)):
            if fps[0] != "/":
                numerator += fps[0]
                fps = fps[1:]
                continue
            fps = fps[1:]
            break

        denominator = fps
        numerator = float(numerator)
        denominator = float(denominator)
        return int(numerator // denominator)
    

def parse_custom_command(commands: str) -> Dict:
    """Parses the custom commands that presets"""
    ret: Dict[str, Any] = {}
    split = [item for item in commands.split(" ") if item and not item.isspace()]
    split.append("-")

    skip_iter: bool = False
    for index in range(len(split) - 1):
        if skip_iter:
            skip_iter = False
            continue
        if split[index][0] == "-" and split[index + 1][0] == "-":
            ret[split[index][1:]] = None
            skip_iter = False
            continue
        if split[index][0] == "-" and split[index + 1][0] != "-":
            ret[split[index][1:]] = split[index + 1]
            skip_iter = True
            continue
        ret[""] = split[index]
    return ret


def get_unnamed_command(presets: List[UnnamedPreset], inpath: str, outpath: str) -> Union[UnnamedPreset, None]:
    """Gets the matching unnamed command from a list of unnamed presets (whether
    an unnamed command is matching is deduced by the file types)
    """
    if "." not in inpath or "." not in outpath:
        return None
    
    in_ext = inpath.split(".")[1]
    out_ext = outpath.split(".")[1]
    for preset in presets:
        if preset.from_type == in_ext and preset.to_type == out_ext:
            return preset
    return None


def get_named_command(presets: List[NamedPreset], name: str) -> Union[NamedPreset, None]:
    """Gets the named command from a list of presets"""
    for preset in presets:
        if preset.name == name:
            return preset
    return None


def convert(arguments: Dict[str, Any]) -> None:
    """High level logic for the conversion"""
    config = load_config()
    named_presets = config[0]
    unnamed_presets = config[1]

    input_path = expand_paths(arguments["module"][0])
    output_path = expand_paths(arguments["module"][1])

    if not os.path.exists(input_path):
        raise ForceExit("input path does not exist")
    if os.path.exists(output_path):
        console.print(f" • specified output path already exists", style="tan")
        console.print(f" • would you like to override the file? (Y/n) ", style="tan", end="")
        affirm = input()
        if not affirm == "Y":
            raise ForceExit("user terminated operation")
        
    preset: Union[NamedPreset, UnnamedPreset, None] = None
    if get_named_command(named_presets, arguments["preset"]) != None and not preset:
        preset = get_named_command(named_presets, arguments["preset"])
        console.print(f" • using matching named preset '{preset.name}'") # type: ignore
        console.print(f" • options applied: '{preset.command}'")  # type: ignore
    if get_unnamed_command(unnamed_presets, input_path, output_path) != None and not preset:
        preset = get_unnamed_command(unnamed_presets, input_path, output_path)
        console.print(f" • using matching unnamed preset ({preset.from_type} to {preset.to_type})") # type: ignore
        console.print(f" • options applied: '{preset.command}'") # type: ignore
    if not preset:
        preset = UnnamedPreset()
        console.print(f" • using default preset because no matching presets were found")
        console.print(f" • no options will be used in the default preset")

    options: Dict = parse_custom_command(preset.command)

    try:
        execute(input_path, output_path, options)
    except FFmpegError as e:
        console.print(f" • mpeg-convert received an ffmpegerror", style="red")
        console.print(f"    - error message from ffmpeg: '{e.message.lower()}'", style="red")
        console.print(f"    - common pitfalls when using ffmpeg/mpeg-convert: ", style="red")
        console.print(f"       * does the output file have an extension? ", style="red")
        console.print(f"       * does the extension match the codec? ", style="red")
        console.print(f"       * is the encoder installed on the system?", style="red")
        raise ForceExit("there was an error with ffmpeg", code=1)


def execute(input_path: str, output_path: str, options: Dict) -> None:
    """Execution of a conversion with an input path, output path, and an options dict"""
    metadata = Metadata(input_path)
    framerate = None
    total_secs = None
    total_frame = None
    try:
        framerate = metadata.get_framerate()
        total_secs = metadata.get_total_secs()
        total_frame = total_secs * framerate
    except ZeroDivisionError:
        console.print(f" • failed retrieving total frames because no video streams were found", style="tan")
        console.print(f"   - mpeg-convert uses total frames to calculate progress", style="tan")
        console.print(f"   - the progress bar will be in an indeterminate state", style="tan")
        console.print(f"   - perhaps you are converting an audio file?", style="tan")

    instance = (
        FFmpeg()
        .option("y")
        .input(input_path)
        .output(
            output_path,
            options
    ))

    last_frame = 0
    start_time = time.time()
    with ProgressBar(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(
            text_format="[progress.percentage]{task.percentage:>0.1f}% ({task.completed}/{task.total} frames)"),
        TextColumn("eta", style="cyan"),
        TimeRemainingColumn(elapsed_when_finished=True),
        console=console,
        transient=True
    ) as bar:
        @instance.on("progress")
        def show_prog(_progress: Progress) -> None:
            nonlocal last_frame
            bar.update(task, total=total_frame)
            bar.update(task, advance=_progress.frame - last_frame)
            last_frame = _progress.frame

        task = bar.add_task("[green]transcoding file...", total=None)
        instance.execute()

    total_time = round(time.time() - start_time, 2)
    total_space = readable_size(output_path)
    console.print(f" • successfully executed mpeg-convert", style="sea_green3")
    console.print(f"    - took {total_time} seconds")
    console.print(f"    - took {total_space} of space")
    console.print(f"    - output file saved to '{output_path}'")



