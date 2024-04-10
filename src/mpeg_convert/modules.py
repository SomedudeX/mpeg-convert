import os

from typing import List, Dict, Any

from .core import help
from .core import version
from .core import convert
from .core import interactive

from .utils import Logger, __version__
from .core.version import get_platform_version, get_python_version
from .arguments import ArgumentsError, parse_arguments, validate_argument_type


def init_logging(argv_properties: Dict[str, Any], argv: List[str]) -> int:
    """Initializes logging and prints some system information for debugging
    purposes.

    Parameters:
        argv_properties: The dictionary to extract log level from
        argv: The arguments to print to the console when outputting system
        information.

    Returns:
        An integer representing the level to log at (requested by the user)
    """
    log_emit_level = Logger.Info

    if argv_properties["debug"]:
        log_emit_level = Logger.Debug
    if argv_properties["quiet"]:
        log_emit_level = Logger.Warning

    log = Logger(emit_level=log_emit_level)
    log.debug(f"Mpeg-convert {__version__}")
    log.debug(f"{get_platform_version()}")
    log.debug(f"{get_python_version(long=True)}")
    log.debug(f"Received arguments: {argv}")
    log.debug(f"Processed properties: {argv_properties}")

    return log_emit_level


def start(argv: List[str]) -> int:
    """Starts the main program by parsing the arguments and initializing
    the correct module. 

    Parameters:
        argv: The arguments from the command-line (usually gotten from
        sys.argv)

    Returns:
        An integer representing the error code
    
    Notes:
        Each module should return an exit code that represents whether it 
        completed successfully.

        This function catches any higher level errors that a module might emit
        such as ArgumentsError and uncaught exceptions (to facilitate a more
        streamlined logging interface). Errors that are module specific should
        be handled at the module level.
    """
    exit_code = 1                 # Default exit code for errors
    log_emit_level = Logger.Info  # Default log emit level

    try:
        argv = argv[1:]
        argv_properties = parse_arguments(argv)
        validate_argument_type(argv_properties)

        log_emit_level = init_logging(argv_properties, argv)
        base_module = argv_properties["module"][0]

        if base_module == "":
            exit_code = help.run_module(argv_properties, log_emit_level)
            return exit_code
        if base_module == "help":
            exit_code = help.run_module(argv_properties, log_emit_level)
            return exit_code
        if base_module == "version":
            exit_code = version.run_module(argv_properties, log_emit_level)
            return exit_code
        if base_module == "convert":
            exit_code = convert.run_module(argv_properties, log_emit_level)
            return exit_code
        if base_module == "interactive":
            exit_code = interactive.run_module(argv_properties, log_emit_level)
            return exit_code
        raise ArgumentsError(f"{base_module} is not a valid command", code=1)
    except ArgumentsError as error:
        log = Logger(log_emit_level)
        log.fatal(f"ArgumentsError: {error.message}")
        log.fatal(f"Mpeg-convert terminating with exit code {error.code}")
        exit_code = error.code
    except KeyboardInterrupt as error:
        log = Logger(log_emit_level)
        log.warning(f"KeyboardInterrupt: Received signal interrupt")
        log.warning(f"Mpeg-convert terminating with os._exit(0)")
        exit_code = 0
        os._exit(0)
    except BaseException as error:
        log = Logger(log_emit_level)
        arguments = " ".join(argv)
        log.fatal(f"An unexpected fatal error occurred: {error}")
        log.fatal(f"Received arguments: '{arguments}'")
        log.fatal(f"Mpeg-convert terminating with exit code -1")
        exit_code = -1
    finally:
        log = Logger(log_emit_level)
        log.debug(f"Modules.start() has finished executing")
        log.debug(f"Returning exit code ({exit_code}) to __main__.main()")
        return exit_code
