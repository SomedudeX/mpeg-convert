"""Custom argument parsing for mpeg-convert"""

import os
import sys

from . import utils

from rich.console import Console


input_path   = ""
output_path  = ""
verbose      = False
default      = False


def _expand_paths() -> None:
    global input_path
    global output_path
    
    Console().log(
        f"[Info] Received file paths: \n'{input_path}', \n'{output_path}'",
        highlight = False
    )
    
    _cwd = os.getcwd() + "/"
    if input_path[0] != "/" and input_path[0] != "~":
        input_path = _cwd + input_path
    if output_path[0] != "/" and output_path[0] != "~":
        output_path = _cwd + output_path
        
    Console().log(
        f"[Info] Parsed file paths: \n'{input_path}', \n'{output_path}'",
        highlight = False
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
        Console().log(f"[yellow][Warning] Using verbose mode", highlight = False)
    if default: 
        Console().log(f"[yellow][Warning] Using all default options", highlight = False)
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
    global default
    
    if value == "--version":
        utils.print_version()
        sys.exit(0)
    elif value == "--customize":
        utils.handle_customize()
        sys.exit(0)
    elif value == "-h" or value == "--help":
        utils.print_help()
        sys.exit(0)
    elif value == "-d" or value == "--default":
        default = True
        return
    elif value == "-v" or value == "--verbose":
        verbose = True
        return
    elif value == "-vd" or value == "-dv":
        default = True
        verbose = True
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
    global default

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
    
    ret = {}
    ret["input"]   = input_path
    ret["output"]  = output_path
    ret["verbose"] = verbose
    ret["default"] = default

    return ret
