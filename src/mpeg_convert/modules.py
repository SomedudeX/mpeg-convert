from typing import Dict, Any

from .exceptions import ArgumentsError
from .core import help
from .core import version
from .core import convert
from .core import interactive


def start(arguments: Dict[Any, Any]) -> int:
    """Starts the main program by initializing the correct module"""
    base_module: str = arguments["module"][0]
    if base_module == "":
        exit_code = help.run_module(arguments)
        return exit_code
    if base_module == "help":
        exit_code = help.run_module(arguments)
        return exit_code
    if base_module == "version":
        exit_code = version.run_module(arguments)
        return exit_code
    if base_module == "convert":
        exit_code = convert.run_module(arguments)
        return exit_code
    if base_module == "interactive":
        exit_code = interactive.run_module(arguments)
        return exit_code
    raise ArgumentsError(f"{base_module} is not a valid command", code=1)
