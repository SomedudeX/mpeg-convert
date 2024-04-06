"""Functions and utility classes that does not fit into other files"""
import os
import sys
import json
import inspect

from rich.console import Console


class ProgramInfo:
    """Information regarding the program should/will be stored here so that it
    can be referred to or changed easily
    """

    VERSION = "v0.2.0"


class CallerInfo:
    """The info of the caller of the function"""
    lineno = -1
    filename = ""


class Logger:
    """A Logger class that prints to the console"""

    Debug   = 1
    Info    = 2
    Warning = 3
    Fatal   = 4

    def __init__(
        self,
        emit_level: int = 2
    ) -> None:
        """Initiates a Logger class

        Args: 
            emit_level: All messages greater than or equal to this level
            (severity) will be emitted when calling the logging methods method
            of this class. 
        """
        self.emit_level = emit_level
        return

    def change_emit_level(
        self,
        new_emit_level: int
    ) -> None:
        """Sets a new emit level; anything above this level will be logged

        Args -
            new_emit_level: A new emit level that all messages greater than or equal
            to this level (severity) will be emitted when calling the logging methods 
            method of this class. """
        self.emit_level = new_emit_level
        return

    def debug(
        self,
        message: str, 
    ) -> None:
        """Log the specified message to the console with `debug` severity

        Args:
            message: The message to log to the console
        """
        caller = get_caller_info()
        header = f"[bright_black]\\[{caller.filename}:{caller.lineno}] \\[Debug]"
        if self.Fatal >= self.emit_level:
            Console().print(f"{header} {message}", highlight=False)
        return

    def info(
        self,
        message: str, 
    ) -> None:
        """Log the specified message to the console with `info` severity

        Args:
            message: The message to log to the console
        """
        caller = get_caller_info()
        header = f"[bright_black]\\[{caller.filename}:{caller.lineno}] [white]\\[Info]"
        if self.Fatal >= self.emit_level:
            Console().print(f"{header} {message}", highlight=False)
        return

    def warning(
        self,
        message: str, 
    ) -> None:
        """Log the specified message to the console with `warning` severity

        Args:
            message: The message to log to the console
        """
        caller = get_caller_info()
        header = f"[bright_black]\\[{caller.filename}:{caller.lineno}] [gold3]\\[Warning]"
        if self.Fatal >= self.emit_level:
            Console().print(f"{header} {message}", highlight=False)
        return

    def fatal(
        self,
        message: str, 
    ) -> None:
        """Log the specified message to the console with the `fatal` severity

        Args:
            message: The message to log to the console
        """
        caller = get_caller_info()
        header = f"[bright_black]\\[{caller.filename}:{caller.lineno}] [red]\\[Fatal]"
        if self.Fatal >= self.emit_level:
            Console().print(f"{header} {message}", highlight=False)
        return


def get_caller_info() -> CallerInfo:
    """Gets the information of the caller of the function via python inspect"""
    stacktrace = inspect.stack()
    frameinfo = inspect.getframeinfo(stacktrace[2][0])
    if sys.platform == "win32":
        filename = frameinfo.filename.split("\\")
    else:
        filename = frameinfo.filename.split("/")
    ret = CallerInfo()
    ret.filename = filename[len(filename) - 1]
    ret.lineno = frameinfo.lineno
    return ret


def expand_paths(path: str) -> str:
    """Expand relative paths or paths with tilde (~) to absolute paths"""
    return os.path.normpath(
        os.path.join(
            os.environ["PWD"], 
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
