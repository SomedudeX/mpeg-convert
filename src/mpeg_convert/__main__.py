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
# This project uses 4 spaces for indentation. import sys

from . import modules
from . import arguments


def main(argv: list[str]) -> int:
    argv_properties = arguments.parse_arguments(argv)
    return modules.start(argv_properties, argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
