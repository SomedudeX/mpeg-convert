#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -*-  Style guide  -*-
#
# This project uses the following styles for token names
#
#     PascalCase       Class name
#     snake_case       Variable or function/method name
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

from .utils import Logger
from .modules import ModulesManager
from .arguments import ArgumentBase
from .arguments import ArgumentParseError, ArgumentValidationError


def main(argv: list[str]) -> int:
    try:                                        # Try-except catches base flag parsing exceptions
        del argv[0]
        root_args = ArgumentBase(argv)          # Parses flags critical to program execution, 
        instance = ModulesManager(root_args)    # then creates an instance of ModulesManager and
        instance.run_module()                   # run the specified module (deducted from arguments)
    except ArgumentValidationError as error:
        console = Logger()
        console.log(f'[red][Fatal] ArgumentValidationError: {error.message}', level=4)
        console.log(f'[Info] Mpeg-convert terminating with exit code {error.code}', level=4)
        return error.code
    except ArgumentParseError as error:
        console = Logger()
        console.log(f'[red][Fatal] ArgumentValidationError: inapt argument \'{error.argument}\'', level=4)
        console.log(f'[Info] Mpeg-convert terminating with exit code {error.code}', level=4)
        return error.code

    console = Logger(root_args.log_level)
    console.log(f'[Info] Mpeg-convert terminating with exit code {instance.exit_code}', level=2)
    return instance.exit_code


if __name__ == '__main__':
    sys.exit(main(sys.argv))
