import os
import sys
import yaml
import platform
import subprocess

from yaml import YAMLError
from rich.console import Console
from typing import Any, Dict, List, Tuple
from ffmpeg import FFmpeg, FFmpegError

from .exceptions import ForceExit, catch

__version__ = "v0.2.0"

# Using the console class from rich to better integrate with its
# progress bar (e.g. printing on top of the progress bar)
console = Console(highlight=False)

ROOT_PATH = "~/.local/share/mpeg-convert/"
MODULE_PATH = os.path.dirname(__file__) + "/"


class NamedPreset:
    """Represents a named conversion preset"""
    name: str = ""
    command: str = ""


class UnnamedPreset:
    """Represents an unnamed conversion preset used automatically"""
    from_type: str = ""
    to_type: str = ""
    command: str = ""


def get_python_version() -> str:
    """Returns basic Python information in a string"""
    return f"{platform.python_implementation()} {platform.python_version()}"


def get_platform_version() -> str:
    """Returns basic OS information in a string"""
    return f"{platform.platform(True, True)} {platform.machine()}"


def check_interactivity() -> None:
    """Checks whether the console is a tty, and print a warning if not"""
    if not (hasattr(sys.stdout, "isatty") or sys.stdout.isatty()):
        console.print(" • warning: mpeg-convert is not being run in a tty")
        console.print(" • warning: some features may not work correctly")


def open_file(filepath: str) -> None:
    """Opens a file with the default application on different platforms. Taken
    from https://stackoverflow.com/questions/434597/open-document-with-default-
    os-application-in-python-both-in-windows-and-mac-os#435669"""
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(filepath) # type: ignore
    else:                                   # Linux variants
        subprocess.call(('xdg-open', filepath))


def expand_paths(path: str) -> str:
    """Expand relative paths or paths with tilde (~) and dot (.) to absolute paths"""
    return os.path.normpath(
        os.path.join(
            os.environ["PWD"],
            os.path.expanduser(path)
    ))


@catch((YAMLError, KeyError, OSError), "an error occurred when reading presets")
def load_config() -> Tuple[List[NamedPreset], List[UnnamedPreset]]:
    """Loads user-defined config from a yaml file into a list"""
    with open(expand_paths(ROOT_PATH + "config.yml"), "r") as f:
        config = yaml.safe_load(f)
        named = []
        unnamed = []
        if "named" in config:
            for item in config["named"]:
                temp = NamedPreset()
                temp.name = item["name"]
                temp.command = item["command"]
                named.append(temp)
        if "unnamed" in config:
            for item in config["unnamed"]:
                temp = UnnamedPreset()
                temp.from_type = item["from-type"]
                temp.to_type = item["to-type"]
                temp.command = item["command"]
                unnamed.append(temp)
        return (named, unnamed)


@catch(FileNotFoundError, "ffmpeg is not installed")
def check_ffmpeg() -> None:
    """Checks whether FFmpeg is installed and on the system path"""
    try:
        ffprobe_instance = FFmpeg(executable="ffprobe").option("h")
        ffmpeg_instance = FFmpeg(executable="ffmpeg").option("h")
        ffprobe_instance.execute()
        ffmpeg_instance.execute()
    except FFmpegError:
        raise ForceExit("ffmpeg is not installed or is corrupted", code=1)
    return


def readable_size(path: str, decimal_points=2) -> str:
    """Calculates the size of a particular file on disk and returns the
    size in a human-readable fashion
    """
    size: float = os.path.getsize(path)
    for i in ["bytes", "kb", "mb", "gb", "tb", "pb"]:
        if size < 1024.0:
            return f"{size:.{decimal_points}f} {i}"
        size /= 1024.0
    return f"{size:.{decimal_points}f} pb"


@catch(OSError, "an error occurred when initializing files and directories")
def initialize(arguments: Dict[str, Any]) -> None:
    """Checks terminal integrity and enables debug logging if applicable"""
    check_interactivity()
    check_ffmpeg()
    if not os.path.exists(expand_paths(ROOT_PATH)):
        os.makedirs(expand_paths(ROOT_PATH))
    if not os.path.exists(expand_paths(ROOT_PATH + "config.yml")):
        with open(expand_paths(MODULE_PATH + "assets/default.yml")) as f:
            default = f.read()
        with open(expand_paths(ROOT_PATH + "config.yml"), "w") as f:
            f.write(default)
    return
