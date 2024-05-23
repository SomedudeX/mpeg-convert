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

import os
import sys
import inspect

from typing import Any, Dict, List

from . import utils
from . import module

from .term import move_caret_newline
from .arguments import parse_arguments
from .exceptions import ArgumentsError, ForceExit, exception_name


def start_module(arguments: Dict[Any, Any]) -> int:
    """Starts the main program by initializing the correct module"""
    if len(arguments["module"]) == 1:
        arg_help = (arguments["help"])
        arg_version = (arguments["version"] and not arguments["help"])
        arg_config = (arguments["config"] and not arg_help and not arg_version)
        if arg_help:
            module.help()
            return 0
        if arg_version:
            module.version()
            return 0
        if arg_config:
            module.config()
            return 0
    if len(arguments["module"]) == 2:
        module.convert(arguments)
        return 0
    raise ArgumentsError("use '--help' for usage info", code=127)


def main(argv: List[str]) -> int:
    try:
        arguments = parse_arguments(argv)
        utils.initialize(arguments)
        return start_module(arguments)
    except KeyboardInterrupt:
        move_caret_newline()
        utils.console.print(f" • mpeg-convert received keyboard interrupt", style="tan")
        utils.console.print(f" • mpeg-convert terminating with exit code 1", style="tan")
        return 1
    except ArgumentsError as e:
        move_caret_newline()
        utils.console.print(f" • mpeg-convert received inapt arguments: {e.arguments}", style="red")
        utils.console.print(f" • mpeg-convert terminating with exit code {e.exit_code}", style="red")
        return e.exit_code
    except ForceExit as e:
        move_caret_newline()
        utils.console.print(f" • mpeg-convert has been interrupted because {e.reason}", style="red")
        utils.console.print(f" • mpeg-convert terminating with exit code {e.exit_code}", style="red")
        return e.exit_code
    except Exception as e:
        move_caret_newline()
        lineno = inspect.trace()[-1].lineno
        function = inspect.trace()[-1].function
        filename = os.path.basename(inspect.trace()[-1].filename)
        utils.console.print(f" • mpeg-convert received an unknown {exception_name(e)}", style="red")
        utils.console.print(f"    - raised by function {function} at {filename}:{lineno}", style="red")
        utils.console.print(f"    - exception cause: {str(e).lower()}", style="red")
        utils.console.print(f" • mpeg-convert terminating with exit code 255", style="red")
        return 255


if __name__ == "__main__":
    sys.exit(main(sys.argv))
