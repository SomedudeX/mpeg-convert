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


from . import utils
from . import modules
from . import arguments


def main(args: list[str]) -> int:
    instance = modules.ModulesManager(args)
    instance.run_module()
    return instance.exit_code


if __name__ == "__main__":
    try:
        root_logger = utils.Logger("__main__.py")
        sys.exit(main(sys.argv))
    except arguments.ArgumentValidationError as error:
        root_logger.log(f"[red][Fatal] ArgumentValidationError: {error.message}")
        root_logger.log(f"[red][Fatal] Mpeg-convert terminating with exit code -1")
        sys.exit(-1)
    except arguments.ArgumentParseError as error:
        root_logger.log(f"[red][Fatal] ArgumentParseError: error parsing '{error.argument}'")
        root_logger.log(f"[red][Fatal] Mpeg-convert terminating with exit code -1")
        sys.exit(-1)
    except Exception as error:
        root_logger.log(f"[red][Fatal] A fatal unknown error occured: {error}")
        root_logger.log(f"[red][Fatal] Mpeg-convert terminating with exit code -1")
        sys.exit(-1)
