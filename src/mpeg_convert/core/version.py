from typing import Any, Dict

from ..arguments import ArgumentsError
from ..utils import __version__, console, logger
from ..utils import get_platform_version, get_python_version


def initialize(arguments: Dict[str, Any]) -> None:
    """Prints local debug messages to the console"""
    if arguments["output"]:
        logger.log("flag output path has been ignored by 'version' command")
    if arguments["output"]:
        logger.log("flag input path has been ignored by 'version' command")
    logger.log("starting module version")
    return


def print_version():
    """Prints the version information to the console"""
    logger.log("gathering system information")
    _prgram_version = __version__.lower()
    _python_version = get_python_version().lower()
    _system_version = get_platform_version().lower()

    console.print(f"program  : {_prgram_version}")
    console.print(f"python   : {_python_version}")
    console.print(f"platform : {_system_version}")
    console.print(f"made with ♡ by zichen")


def run_module(argv: Dict[str, Any]) -> int:
    """Runs the version module (command)"""
    initialize(argv)
    if argv["module"] == ["version"]:
        print_version()
        return 0
    raise ArgumentsError(
        f"invalid positional argument(s) '{' '.join(argv['module'])}' " + 
        f"received by version command", code=16
    )
    
