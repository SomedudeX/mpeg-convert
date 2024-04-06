import os

from typing import List

from .core import help
from .core import version
from .core import convert
from .core import interactive

from .exceptions import *
from .utils import Logger
from .arguments import parse_arguments


def start(argv: List[str]) -> int:
    """Starts the main program by parsing the arguments and initializing
    the correct module. 

    Returns:
        An integer representing the error code
    
    Notes:
        Each module should return an exit code that represents whether it 
        completed succesfully. 

        This function catches any higher level errors that a module might emit
        such as ModuleErrors and uncaught exceptions (so as to facilitate a
        more streamlined logging interface). Errors that are module specific
        should be handled at the module level. 
    """
    try:
        argv = argv[1:]
        argv_properties = parse_arguments(argv)
        module = argv_properties["module"]
        if module[0] == "":
            return help.run_module(argv_properties, module)
        if module[0] == "help":
            return help.run_module(argv_properties, module)
        if module[0] == "version":
            return version.run_module(argv_properties, module)
        if module[0] == "convert":
            return convert.run_module(argv_properties, module)
        if module[0] == "interactive":
            return interactive.run_module(argv_properties, module)
        raise ModuleError(f"{module[0]} is not a valid command", code=64)
    except ModuleError as error:
        log = Logger()
        log.fatal(f"ModuleError: {error.message}")
        log.fatal(f"Mpeg-convert terminating with exit code {error.code}")
        return error.code
    except ArgumentsError as error:
        log = Logger()
        log.fatal(f"ArgumentsError: {error.message}")
        log.fatal(f"Mpeg-convert terminating with exit code {error.code}")
        return error.code
    except KeyboardInterrupt as error:
        log = Logger()
        log.warning(f"KeyboardInterrupt: Received signal interrupt")
        log.warning(f"Mpeg-convert terminating with os._exit()")
        os._exit(0)
    except BaseException as error:
        log = Logger()
        arguments = " ".join(argv)
        log.fatal(f"An unexpected fatal error occured: {error}")
        log.fatal(f"Received arguments: '{arguments}'")
        log.fatal(f"Mpeg-convert terminating with exit code -1")
        return -1
