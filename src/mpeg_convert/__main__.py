#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This project requires Python 3.9+ to run

# -*-  Style guide  -*-
#
# This project uses the following styles for token names
#
#     PascalCase       Class name
#     snake_case       Variable or function/method name
#     _underscore      Private attribute
#
# Because python does not have a reliable way of signalling the end
# of a particular scope, method, or class, any class/method in this
# file will always terminate in `return` regardless of the return
# type.
#
# In addition, python's native type hinting is used whenever possible
# in order to catch issues and minimize problems with static analyzers
#
# This project uses 4 spaces for indentation.

import sys

from typing import Any, Dict, List

from . import utils

from .core import help
from .core import version
from .core import console
from .core import interactive

from .term import move_caret_newline
from .arguments import parse_arguments
from .exceptions import ArgumentsError, ForceExit, exception_name


def start_module(arguments: Dict[Any, Any]) -> int:
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
    if base_module == "console":
        exit_code = console.run_module(arguments)
        return exit_code
    if base_module == "interactive":
        exit_code = interactive.run_module(arguments)
        return exit_code
    raise ArgumentsError(f"{base_module} is not a valid command", code=2)


def main(argv: List[str]) -> int:
    try:
        arguments = parse_arguments(argv)
        utils.initialize(arguments)
        return start_module(arguments)
    except KeyboardInterrupt:
        move_caret_newline()
        utils.console.print(f" • mpeg-convert received keyboard interrupt")
        utils.console.print(f" • mpeg-convert terminating with exit code 1")
        return 1
    except ArgumentsError as e:
        move_caret_newline()
        utils.console.print(f" • mpeg-convert received inapt arguments: {e.arguments}")
        utils.console.print(f" • mpeg-convert terminating with exit code {e.exit_code}")
        return e.exit_code
    except ForceExit as e:
        move_caret_newline()
        utils.debug.log(f"an exception has been encountered")
        utils.debug.log(f"the exception details will be printed below")
        utils.debug.log(f"{exception_name(e.original)} — {str(e.original).lower()}")
        utils.console.print(f" • mpeg-convert has been interrupted because {e.reason}")
        utils.console.print(f" • mpeg-convert terminating with exit code {e.exit_code}")
        return e.exit_code
    except Exception as e:
        move_caret_newline()
        utils.debug.log(f"an exception has been encountered")
        utils.debug.log(f"the exception details will be printed below")
        utils.debug.log(f"{exception_name(e)} — {str(e).lower()}")
        utils.console.print(f" • mpeg-convert received an unknown {exception_name(e)}")
        utils.console.print(f" • mpeg-convert terminating with exit code 255")
        return -1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
