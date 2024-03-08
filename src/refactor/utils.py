import os
import json

from rich.console import Console

from .argparse import ArgumentBase, ArgumentValidationError


def log(message: str, print: bool = True) -> None:
    """Logs a message to the console via rich
    
    + Args -
        message: The message to print
        print: Whether to print the message (used to enable verbose)
    """
    if print:
        Console(highlight = False).log(message)
        return


def expand_paths(path: str) -> str:
    """Expand relative paths or paths with tilde (~) to absolute paths"""
    return os.path.normpath(
        os.path.join(
            os.environ['PWD'], 
            os.path.expanduser(path)
        )
    )


def create_json(path: str) -> None:
    """Create a json file if it does not already exist"""
    if not os.path.exists(path):
        file = open(path, "w")
        json.dump([], file)
        file.close()
    return


def validate_arguments(arguments: ArgumentBase):
    """Check parsed command-line arguments for validity (e.g. file path exists,
    no conflicting arguments, etc.)
    
    + Args -
        arguments: An ArgumentBase class that represents command-line args
    """
    if arguments.input_file == "":
        raise ArgumentValidationError("no input file specified")
    if arguments.output_file == "":
        raise ArgumentValidationError("no output file specified")
    if not os.path.isfile(arguments.input_file):
        raise ArgumentValidationError("specified input file invalid")
        
    if arguments.make_preset and arguments.list_preset:
        raise ArgumentValidationError("conflicting arguments '--preset-make and --preset-list'")
    if arguments.make_preset and arguments.dump_preset:
        raise ArgumentValidationError("conflicting arguments '--preset-make and --preset-dump'")
    if arguments.list_preset and arguments.dump_preset:
        raise ArgumentValidationError("conflicting arguments '--preset-list and --preset-dump'")
    if arguments.make_preset and arguments.list_preset and arguments.dump_preset:
        raise ArgumentValidationError("conflicting arguments '--preset-make, --preset-list, and --preset-dump'")
        
