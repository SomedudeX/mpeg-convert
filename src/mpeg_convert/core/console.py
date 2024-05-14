from typing import Any, Dict

from ..exceptions import ArgumentsError
from ..utils import debug, load_presets


def initialize(arguments: Dict[str, Any]) -> None:
    """Prints local debug messages to the console"""
    debug.log("starting module console")
    return





def run_module(argv: Dict[Any, Any]) -> int:
    """Runs the console module (command)"""
    initialize(argv)
    if argv == ["console", "convert"]:
        ...
        return 0
    if argv == ["console", "create"]:
        ...
        return 0
    if argv == ["console", "delete"]:
        ...
        return 0
    raise ArgumentsError(
        f"invalid positional argument(s) '{' '.join(argv['module'])}' " + 
        f"received by version command", code=2
    )
