import os

from typing import Any, Dict, List

from ..exceptions import ArgumentsError
from ..utils import Preset, console, debug, MODULE_PATH
from ..utils import load_presets, write_presets

from rich import box
from rich.table import Table
from ffmpeg import FFmpeg, FFmpegError, FFmpegInvalidCommand


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
    
    debug.log(f"parsed custom command: {ret}")
    return ret


def is_valid_preset_name(name: str) -> bool:
    """Checks if a preset name is valid"""
    for char in name:
        is_valid_char = (
            char == "-" or char == "_" or \
            char.isalpha() or char.isdigit())
        if not is_valid_char:
            return False
    return len(name) != 0 and name[0] != "_"


def is_valid_preset_command(command: str) -> bool:
    """Checks if an ffmpeg command is valid by executing it"""
    try:
        parsed_options = parse_custom_command(command)
        debug.log(f"checking preset command validity by test running ffmpeg")
        instance = FFmpeg()
        instance.input(MODULE_PATH + "assets/sample_in.mp4")
        instance.output(MODULE_PATH + "assets/sample_out.mp4", parsed_options)
        instance.execute()
        return True
    except FFmpegInvalidCommand as e:
        e.message = e.message.lower()
        e.arguments = [arg.lower() for arg in e.arguments]
        debug.log(f"ffmpeg raised invalid command exception")
        debug.log(f"error message from ffmpeg: {e.message}")
        return False
    except FFmpegError as e:
        e.message = e.message.lower()
        e.arguments = [arg.lower() for arg in e.arguments]
        debug.log(f"ffmpeg raised generic ffmpeg error")
        debug.log(f"error message from ffmpeg: {e.message}")
        return False
    finally:
        if os.path.exists(MODULE_PATH + "assets/sample_out.mp4"):
            debug.log(f"removing test sample output file")
            os.remove(MODULE_PATH + "assets/sample_out.mp4")


def ask_preset_name(message: str) -> str:
    """Asks the user for input, then validates the input"""
    while True:
        console.print(message, end="")
        value = input()
        if not is_valid_preset_name(value):
            console.print(f" • please enter a valid preset name", style="red")
            console.print(f"    - spaces or leading underscores are not allowed", style="red")
            console.print(f"    - valid characters are 'A-z', dashes, and underscores", style="red")
            continue
        return value


def ask_preset_command(message: str) -> str:
    """Asks the user for input, then validates the input"""
    while True:
        console.print(message, end="")
        value = input()
        if not is_valid_preset_command(value):
            console.print(f" • please enter valid ffmpeg commands", style="red")
            console.print(f"    - make sure the options are formatted correctly", style="red")
            console.print(f"    - make sure the options are supported on your platform", style="red")
            continue
        return value
    return


def console_create(arguments: Dict[str, Any]) -> None:
    """Runs the preset creation tool"""
    new_preset = Preset()
    presets: List[Preset] = load_presets()
    console.print(f" • mpeg-convert preset creator tool")
    new_preset.name = ask_preset_name(f" > enter the name of the new preset: ")
    new_preset.command = ask_preset_command(f" > enter ffmpeg options for the new preset: ")

    summary_table = Table(box=box.SQUARE)
    summary_table.add_column("Name", min_width=20)
    summary_table.add_column("Options", min_width=60)
    for preset in presets:
        summary_table.add_row(preset.name, preset.command)
    summary_table.add_row(new_preset.name + " (created)", new_preset.command, style="blue")

    presets.append(new_preset)
    write_presets(presets)
    console.print(f" • mpeg-convert preset creator tool summary")
    console.print(summary_table)


def run_module(argv: Dict[Any, Any]) -> int:
    """Runs the console module (command)"""
    debug.log("starting module console")
    if argv["module"] == ["console", "convert"]:
        ...
        return 0
    if argv["module"] == ["console", "create"]:
        console_create(argv)
        return 0
    if argv["module"] == ["console", "delete"]:
        ...
        return 0
    raise ArgumentsError(
        f"invalid positional argument(s) '{' '.join(argv['module'])}' " + 
        f"received by console command", code=2
    )
