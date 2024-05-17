import os
import sys
import json
import platform

from json import JSONDecodeError
from rich.console import Console
from typing import Any, Dict, List

from .exceptions import catch
from .term import Logger

__version__ = "v0.2.0"

# Using the console class from rich to better integrate with its
# progress bar (e.g. printing on top of the progress bar)
console = Console(highlight=False)
debug = Logger(highlight=False)

ROOT_PATH = "~/.local/share/mpeg-convert/"
MODULE_PATH = os.path.dirname(__file__) + "/"


class Preset:
    """Represents a conversion preset"""
    name: str = ""
    command: str = ""

    def __repr__(self) -> str:
        return f"+ {self.name}" + " " * (10 - len(self.name)) + f"{self.command}"
    
    def dict(self) -> dict:
        return { "name": self.name, "command": self.command }


def get_python_version() -> str:
    """Returns basic Python information in a string"""
    return f"{platform.python_implementation()} {platform.python_version()}"


def get_platform_version() -> str:
    """Returns basic OS information in a string"""
    return f"{platform.platform(True, True)} {platform.machine()}"


def check_interactivity():
    """Checks whether the console is a tty, and print a warning if not"""
    if not (hasattr(sys.stdout, "isatty") or sys.stdout.isatty()):
        console.print(" • warning: mpeg-convert is not being run in a tty")
        console.print(" • warning: some features may not work correctly")


def enable_debug() -> None:
    """Enables debug mode globally and prints debug headers"""
    debug.quiet = False
    debug.log(f"mpeg-convert {__version__}")
    debug.log(get_python_version().lower())
    debug.log(get_platform_version().lower())
    return


def expand_paths(path: str) -> str:
    """Expand relative paths or paths with tilde (~) and dot (.) to absolute paths"""
    return os.path.normpath(
        os.path.join(
            os.environ["PWD"],
            os.path.expanduser(path)
        )
    )


@catch((JSONDecodeError, KeyError, OSError), "an error occurred when reading presets")
def load_presets() -> List[Preset]:
    """Loads user-defined preset from a json file into a list"""
    ret = []
    debug.log(f"reading user-defined presets:")
    with open(expand_paths(ROOT_PATH + "preset.json"), "r") as preset:
        presets = json.load(preset)
        for preset in presets:
            current_preset = Preset()
            current_preset.name = preset["name"]
            current_preset.command = preset["command"]
            ret.append(current_preset)
            debug.log(f"{current_preset}")
    return ret


@catch(OSError, "an error occured when writing presets")
def write_presets(presets: List[Preset]) -> None:
    """Write a list of preset into a json file"""
    dict_presets = [preset.dict() for preset in presets]
    debug.log("opening presets.json to write presets to disk")
    with open(expand_paths(ROOT_PATH + "preset.json"), "w") as f:
        json.dump(dict_presets, f)
    return


@catch(OSError, "an error occurred when initializing files and directories")
def initialize(arguments: Dict[str, Any]) -> None:
    """Checks terminal integrity and enables debug logging if applicable"""
    check_interactivity()
    if arguments["debug"]:
        enable_debug()
    if not os.path.exists(expand_paths(ROOT_PATH)):
        os.makedirs(expand_paths(ROOT_PATH))
    if not os.path.exists(expand_paths(ROOT_PATH + "preset.json")):
        with open(expand_paths(MODULE_PATH + "assets/default.json")) as f:
            default = json.load(f)
        with open(expand_paths(ROOT_PATH + "preset.json"), "w") as f:
            json.dump(default, f)
    return
