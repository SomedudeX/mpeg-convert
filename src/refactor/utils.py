"""Functions and utility classes that does not fit into other files"""
import os
import json

from datetime import datetime
from rich.console import Console


class Logger:
    """"""

    def __init__(
        self,
        name: str,
        emit_level: int = 1
    ) -> None:
        """Initiates a Logger class

         + Args - 
            name: The name of the logger to be printed when logging
            emit_level: All messages greater than or equal to this level (severity) will
            be emitted when calling the `log` method of this class. """
        self.name = name
        self.emit_level = emit_level
        return

    def log(
        self,
        message: str, 
        level: int = 2
    ) -> None:
        """Log the specified message to the console with specified severity

         + Args -
            message: The message to log to the console
            level: The level of severity to log at. Program uses the following
            scale —— 1 (debug), 2 (info), 3 (fatal). """
        if level >= self.emit_level:
            time = datetime.now().strftime("%H:%M:%S")
            Console().print(f"[{time}] [{self.name}] {message}", )


def expand_paths(path: str) -> str:
    """Expand relative paths or paths with tilde (~) to absolute paths"""
    return os.path.normpath(
        os.path.join(
            os.environ['PWD'], 
            os.path.expanduser(path)
        )
    )


def create_json(path: str) -> None:
    """Create a json file if it does not already exist"""
    if not os.path.exists(path):
        file = open(path, "w")
        json.dump([], file)
        file.close()
    return
