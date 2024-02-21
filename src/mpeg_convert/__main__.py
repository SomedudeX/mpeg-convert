#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -*-  Style guide  -*-
#
# This project uses the following styles for token names
#
#     PascalCase       Class name
#     snake_case       Variable or function/method name
#     _underscore      Variable/function should be used only internally in
#                      the scope it's declared in (and should not be
#                      modified by the end user)
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


from src.mpeg_convert.utils import ModuleCheck

# Check module health before importing
ModuleCheck.check_required()
ModuleCheck.check_customize()

import os
import sys

from rich import traceback
from rich.console import Console

from src.mpeg_convert.convert import Program
from src.mpeg_convert.utils import FatalError


def main():
    _printer = Console(highlight=False)
    _err_printer = Console(highlight=False, style="red")
    traceback.install()

    try:
        instance = Program()
        instance.run()
    except FatalError as e:
        _err_printer.log(f"{e.msg}")
        _err_printer.log(f"{e.note}")
        _err_printer.log(f"[Info] Mpeg-convert terminating with exit code {e.code}")
        sys.exit(1)
    except KeyboardInterrupt:
        _printer.print()
        _printer.log("[yellow][Warning] Mpeg-convert received KeyboardInterrupt")
        _printer.log("[yellow][Warning] Force quitting with os._exit()")
        os._exit(0)


if __name__ == "__main__":
    main()
