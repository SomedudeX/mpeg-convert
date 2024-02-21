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


from mpeg_convert.utils import ModuleCheck

# Check module health before importing
ModuleCheck.check_required()
ModuleCheck.check_customize()

import os
import sys

from rich import traceback
from rich.console import Console

from mpeg_convert.convert import Program
from mpeg_convert.utils import FatalError


def main():
    _printer = Console(highlight=False)
    traceback.install()

    try:
        instance = Program()
        instance.run()
    except FatalError as e:
        _printer.log(f"[red]{e.msg}")
        _printer.log(f"[red]{e.note}")
        _printer.log(f"[Info] Mpeg-convert terminating with exit code {e.code}")
        sys.exit(1)
    except KeyboardInterrupt:
        _printer.print("\n")
        _printer.log("[yellow][Warning] Mpeg-convert received KeyboardInterrupt")
        _printer.log("[yellow][Warning] Force quitting with os._exit()")
        os._exit(0)


if __name__ == "__main__":
    main()
