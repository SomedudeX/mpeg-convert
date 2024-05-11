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

import re
import sys

from typing import List

from . import utils
from . import modules

from .utils import console
from .term import move_caret_newline
from .arguments import parse_arguments
from .exceptions import ArgumentsError, ForceExit


def main(argv: List[str]) -> int:
    try:
        arguments = parse_arguments(argv)
        utils.initialize(arguments)
        return modules.start(arguments)
    except KeyboardInterrupt:
        move_caret_newline()
        console.print(f" • mpeg-convert received keyboard interrupt")
        console.print(f" • mpeg-convert terminating with exit code 1")
        return 1
    except ArgumentsError as e:
        console.print(f" • mpeg-convert received inapt arguments: {e.message}")
        console.print(f" • mpeg-convert terminating with exit code {e.code}")
        return e.code
    except ForceExit as e:
        console.print(f" • mpeg-convert has been interrupted because {e.reason}")
        console.print(f" • mpeg-convert terminating with exit code {e.code}")
        return e.code
    except Exception as e:
        name = re.sub(r"(?<!^)(?=[A-Z])", " ", type(e).__name__).lower()
        move_caret_newline()
        console.print(f" • mpeg-convert received an unknown {name}")
        console.print(f" • mpeg-convert terminating with exit code 255")
        return 255
    return


if __name__ == "__main__":
    sys.exit(main(sys.argv))
