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
from . import argparse
# from .modules import modules


def main():
    arguments_handler = argparse.ArgumentsHandler(sys.argv)
    arguments = arguments_handler.process_args()
    
    utils.validate_arguments(arguments)
    
    # modules_handler = modules.ModulesHandler(arguments)
    # modules_handler.run_module()
    
    # return modules_handler.get_exit_code()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except argparse.ArgumentParseError as e:
        utils.log(f"[red][Fatal] ArgumentParseError: argument '{e.arguments}' is invalid")
        utils.log(f"[red][Fatal] Mpeg-convert terminating with exit code -1")
        sys.exit(-1)
    except argparse.ArgumentValidationError as e:
        utils.log(f"[red][Fatal] ArgumentValidationError: {e.message}")
        utils.log(f"[red][Fatal] Mpeg-convert terminating with exit code -1")
        sys.exit(-1)
