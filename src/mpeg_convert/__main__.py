#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .utils import ModuleCheck

# Check module health before importing
ModuleCheck.check_required()
ModuleCheck.check_customize()


import os
import sys

from rich import traceback
from rich.console import Console

from .convert import Program
from .utils import FatalError
    

def main():
    _printer     = Console(highlight = False)
    _err_printer = Console(highlight = False, style = "red")
    traceback.install()
    
    try:
        instance = Program()
        instance.run()
    except FatalError as e:
        _err_printer.log(f"{e.msg}")
        _err_printer.log(f"{e.note}")
        _err_printer.log(f"[Info] Mpeg-convert terminating with exit code {e.code}")
        sys.exit(1)
    except KeyboardInterrupt as e:
        _printer.print()
        _printer.log("[yellow][Warning] Mpeg-convert received KeyboardInterrupt")
        _printer.log("[yellow][Warning] Force quitting with os._exit()")
        os._exit(0)


if __name__ == "__main__":
    main()
