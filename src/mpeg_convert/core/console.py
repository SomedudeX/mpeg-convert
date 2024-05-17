import os

from typing import Any, Dict, List

from ..exceptions import ArgumentsError, ForceExit
from ..utils import Preset, console, debug, MODULE_PATH
from ..utils import load_presets, write_presets

from rich import box
from rich.table import Table
from ffmpeg import FFmpeg, FFmpegError


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


#############################################
## Console create preset                   ##
#############################################


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
    except FFmpegError as e:
        debug.log(f"ffmpeg raised generic ffmpeg error")
        debug.log(f"error message from ffmpeg: {e.message.lower()}")
        return False
    finally:
        if os.path.exists(MODULE_PATH + "assets/sample_out.mp4"):
            debug.log(f"removing test sample output file")
            os.remove(MODULE_PATH + "assets/sample_out.mp4")


def ask_preset_name() -> str:
    """Asks the user for input, then validates the input"""
    while True:
        console.print(f" > enter the name of the new preset: ", end="")
        value = input()
        if not is_valid_preset_name(value):
            console.print(f" • please enter a valid preset name", style="red")
            console.print(f"    - spaces or leading underscores are not allowed", style="red")
            console.print(f"    - valid characters are 'A-z', dashes, and underscores", style="red")
            continue
        return value


def ask_preset_command() -> str:
    """Asks the user for input, then validates the input"""
    while True:
        console.print(f" > enter ffmpeg options for the new preset: ", end="")
        value = input()
        if not is_valid_preset_command(value):
            console.print(f" • please enter valid ffmpeg commands", style="red")
            console.print(f"    - make sure the options are formatted correctly", style="red")
            console.print(f"    - make sure the options are supported on your platform", style="red")
            continue
        return value

def console_create(arguments: Dict[str, Any]) -> None:
    """Runs the preset creation tool"""
    new_preset = Preset()
    presets: List[Preset] = load_presets()
    console.print(f" • mpeg-convert preset creator tool")
    new_preset.name = ask_preset_name()
    new_preset.command = ask_preset_command()

    for preset in presets:
        if preset.name == new_preset.name:
            console.print(f" • preset name already taken in existing presets", style="tan")
            console.print(f" > would you like to override the original command? (Y/n) ", style="tan", end="")
            value = input()
            if not value == "Y":
                raise ForceExit("user cancelled action")
            preset.command = new_preset.command
            break
    else:
        presets.append(new_preset)

    write_presets(presets)
    console.print(f" • succesfully created preset '{new_preset.name}'")
    return


def initialize_create(arguments: Dict[str, Any]) -> None:
    if arguments["input"]:
        debug.log("flag input path has been ignored by 'console create' command")
    if arguments["output"]:
        debug.log("flag output path has been ignored by 'console create' command")
    if arguments["preset"]:
        debug.log("flag preset has been ignored by 'console create' command")
    debug.log("starting module 'console create'")
    return


#############################################
## Console delete preset                   ##
#############################################


def ask_preset_delete(current_presets: List[Preset]) -> int:
    while True:
        console.print(f" > enter the name of the preset to delete: ", end="")
        value = input()
        debug.log(f"verifying whether preset name exist")
        if not value in [preset.name for preset in current_presets]:
            console.print(f" • please a valid preset name", style="red")
            console.print(f"    - make sure the preset name is formatted correctly", style="red")
            console.print(f"    - make sure the preset name exist in the current presets", style="red")
            continue
        debug.log(f"returning delete index")
        for index, preset in enumerate(current_presets):
            if preset.name == value:
                return index


def console_delete(arguments: Dict[str, Any]) -> None:
    presets: List[Preset] = load_presets()
    console.print(f" • mpeg-convert preset deleter tool")
    delete_index = ask_preset_delete(presets)
    console.print(f" • succesfully deleted preset '{presets[delete_index].name}'")
    del presets[delete_index]
    write_presets(presets)
    return


def initialize_delete(arguments: Dict[str, Any]) -> None:
    if arguments["input"]:
        debug.log("flag input path has been ignored by 'console delete' command")
    if arguments["output"]:
        debug.log("flag output path has been ignored by 'console delete' command")
    if arguments["preset"]:
        debug.log("flag preset has been ignored by 'console delete' command")
    debug.log("starting module 'console delete'")
    return


#############################################
## Console list preset                     ##
#############################################


def create_table(presets: List[Preset]) -> Table:
    summary_table = Table(box=box.HEAVY_EDGE)
    summary_table.add_column("name", min_width=20)
    summary_table.add_column("options", min_width=60)
    for preset in presets:
        command = preset.command if preset.command else "no options"
        summary_table.add_row(preset.name, command)
    return summary_table


def initialize_list(arguments: Dict[str, Any]) -> None:
    if arguments["input"]:
        debug.log("flag input path has been ignored by 'console list' command")
    if arguments["output"]:
        debug.log("flag output path has been ignored by 'console list' command")
    if arguments["preset"]:
        debug.log("flag preset has been ignored by 'console list' command")
    debug.log("starting module 'console list'")
    return


def console_list(arguments: Dict[str, Any]) -> None:
    presets: List[Preset] = load_presets()
    console.print(f" • current user defined mpeg-convert presets")
    console.print(create_table(presets))
    return


def run_module(argv: Dict[Any, Any]) -> int:
    """Runs the console module (command)"""
    if argv["module"] == ["console", "convert"]:
        ...
        return 0
    if argv["module"] == ["console", "create"]:
        initialize_create(argv)
        console_create(argv)
        return 0
    if argv["module"] == ["console", "delete"]:
        initialize_delete(argv)
        console_delete(argv)
        return 0
    if argv["module"] == ["console", "list"]:
        initialize_list(argv)
        console_list(argv)
        return 0
    raise ArgumentsError(
        f"invalid positional argument(s) '{' '.join(argv['module'])}' " + 
        f"received by console command", code=2
    )
