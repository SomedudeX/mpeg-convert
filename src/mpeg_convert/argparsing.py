"""Custom argument parsing for mpeg-convert"""

import os
import sys

from mpeg_convert import utils
from mpeg_convert.customization import *

from rich.console import Console

input_path = ""
output_path = ""
verbose = False
options = {}

_option_name = ""


def _expand_paths() -> None:
    global input_path
    global output_path

    if verbose:
        Console().log(
            f"[Info] Received file paths: \n'{input_path}', \n'{output_path}'",
            highlight=False
        )

    _cwd = os.getcwd() + "/"
    if input_path[0] != "/" and input_path[0] != "~":
        input_path = _cwd + input_path
    if output_path[0] != "/" and output_path[0] != "~":
        output_path = _cwd + output_path

    if verbose:
        Console().log(
            f"[Info] Parsed file paths: \n'{input_path}', \n'{output_path}'",
            highlight=False
        )

    return


def _validate_paths() -> None:
    global input_path
    global output_path

    if len(input_path) == 0:
        raise Exception(f"input file path not specified")
    if len(output_path) == 0:
        raise Exception(f"output file path not specified")
    if not os.path.isfile(input_path):
        raise Exception(f"input path '{input_path}' is invalid")

    if verbose:
        Console().log(f"[yellow][Warning] Using verbose mode", highlight=False)
    if options:
        Console().log(f"[yellow][Warning] Using custom preset options ('{_option_name}')", highlight=False)
    return


def _parse_positional(value: str) -> None:
    global input_path
    global output_path

    if len(input_path) == 0:
        input_path = value
        return
    if len(output_path) == 0:
        output_path = value
        return
    raise Exception(f"unexpected trailing argument '{value}'")


def _parse_flag(value: str) -> None:
    global verbose
    global options
    global _option_name

    if value == "--version":
        utils.print_version()
        sys.exit(0)
    elif value == "--customize":
        utils.handle_customize()
        sys.exit(0)
    elif value == "-h" or value == "--help":
        utils.print_help()
        sys.exit(0)
    elif value == "-v" or value == "--verbose":
        verbose = True
        return
    elif value[2:] in PRESETS:
        _option_name = value[2:]
        options = PRESETS[value[2:]]
        return
    else:
        raise Exception(f"unrecognized option '{value}'")


def parse_args() -> dict:
    """Parses the command-line arguments from the user.
    
    The path to the current working directories will be appended to
    the input and output arguments if they are relative paths. This
    is because the python-ffmpeg module does not operate in relative
    paths. 

    Commands can be listed with the option `-h` or `--help`. 
    """

    global input_path
    global output_path
    global verbose
    global options

    if len(sys.argv) == 1:
        utils.print_help()
        sys.exit(0)

    is_flag = True
    for index, value in enumerate(sys.argv):
        if index == 0:
            continue
        if value[0] != "-":
            is_flag = False
        if is_flag == True:
            _parse_flag(value)
        if is_flag == False:
            _parse_positional(value)

    _validate_paths()
    _expand_paths()

    ret = {
        "input": input_path,
        "output": output_path,
        "verbose": verbose,
        "options": options
    }

    return ret
