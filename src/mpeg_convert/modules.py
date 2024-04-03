from .core import help
from .core import version
from .core import convert
from .core import interactive

from .utils import Logger
from .arguments import ProgramArguments, AvailableModules


class ModuleError(Exception):
    
    def __init__(
        self, 
        message: str,
        code: int = 1
    ) -> None:
        self.message = message
        self.code = code
        super().__init__()


def start(argv_properties: ProgramArguments, argv: list[str]) -> int:
    try:
        if argv_properties.module == "":
            return help.run_module(argv_properties, argv)
        if argv_properties.module == "help":
            return help.run_module(argv_properties, argv)
        if argv_properties.module == "version":
            return version.run_module(argv_properties, argv)
        if argv_properties.module == "convert":
            return convert.run_module(argv_properties, argv)
        if argv_properties.module == "interactive":
            return interactive.run_module(argv_properties, argv)
        if argv_properties.module not in AvailableModules:
            raise ModuleError(f"{argv_properties.module} is not a valid command", code=64)
    except ModuleError as error:
        log = Logger()
        log.fatal(f"ModuleError: {error.message}")
        log.fatal(f"Mpeg-convert terminating with exit code {error.code}")
        return error.code
    except BaseException as error:
        log = Logger()
        log.fatal(f"An unexpected fatal error occured: {error}")
        log.fatal(f"Mpeg-convert terminating with exit code -1")
        return -1
