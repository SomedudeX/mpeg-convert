import sys
import platform

from typing import Any, Dict

from ..utils import __version__, Logger
from ..arguments import ArgumentsError

log = Logger()


def get_python_version(long: bool = False) -> str:
    if not long:
        return f"{platform.python_version()}"
    return f"{platform.python_implementation()} {sys.version}"


def get_platform_version() -> str:
    return f"{platform.platform(True, True)} {platform.machine()}"


def print_version():
    """Prints the version information to the console"""
    _prgram_version = __version__
    _python_version = get_python_version()
    _system_version = get_platform_version()

    print(f"Program  : {_prgram_version}")
    print(f"Python   : {_python_version}")
    print(f"Platform : {_system_version}")
    print(f"Made with ♡ by Zichen")


def validate_arguments(argv_properties: Dict[str, Any], log_level: int) -> None:
    if len(argv_properties["module"]) > 1:
        raise ArgumentsError(f"unexpected positional argument '{argv_properties["module"][1]}'", code=65)
    if argv_properties["preset"] != "":
        raise ArgumentsError(f"unsupported option preset for command 'version'", code=65)
    log.change_emit_level(log_level)
    log.debug("Finished module level arguments parsing")


def run_module(argv: Dict[str, Any], log_level: int) -> int:
    validate_arguments(argv, log_level)
    print_version()
    return 0
