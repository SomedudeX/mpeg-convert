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

root_path = "~/.local/share/mpeg-convert"
preset_path = "~/.local/share/mpeg-convert/preset.json"


class Preset:
    """Represents a user-defined conversion preset"""
    name: str
    command: str


def get_python_version() -> str:
    """Returns basic Python information in a string"""
    return f"{platform.python_implementation()} {platform.python_version()}"


def get_platform_version() -> str:
    """Returns basic OS information in a string"""
    return f"{platform.platform(True, True)} {platform.machine()}"


def check_tty():
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


def create_folder(path: str) -> None:
    """Create a folder if it does not already exist"""
    if not os.path.exists(path):
        os.makedirs(path)
    return


def create_json(path: str) -> None:
    """Create a json file if it does not already exist"""
    if not os.path.exists(path):
        file = open(path, "w")
        json.dump([], file)
        file.close()
    return


def expand_paths(path: str) -> str:
    """Expand relative paths or paths with tilde (~) to absolute paths"""
    return os.path.normpath(
        os.path.join(
            os.environ["PWD"],
            os.path.expanduser(path)
        )
    )


@catch((JSONDecodeError, KeyError), "an error occurred when reading presets")
def load_presets() -> List[Preset]:
    ret = []
    with open(expand_paths(preset_path), "r") as preset:
        presets = json.load(preset)
        for preset in presets:
            current_preset = Preset()
            current_preset.name = preset["name"]
            current_preset.command = preset["command"]
            ret.append(current_preset)
    return ret


def initialize(arguments: Dict[str, Any]) -> None:
    """Checks terminal integrity and enables debug logging if applicable"""
    check_tty()
    create_folder(expand_paths(root_path))
    create_json(expand_paths(preset_path))
    if arguments["debug"]:
        enable_debug()
    return
