"""The central hub for launching, managing, and closing modules"""

from .utils import Logger
from .exceptions import BaseError
from .arguments import ArgumentBase, AvailableModules
from .arguments import ArgumentValidationError, ArgumentParseError

from .core import help
from .core import version
from .core import convert
from .core import presets


class ModulesManager:
    """Manages launching, running, and closing modules"""
    
    def __init__(
        self,
        arguments_list: ArgumentBase,
    ) -> None:
        """Initializes a ModulesManager object

         + Args - 
            arguments_list: The list of arguments to pass to the module (most likely sys.argv)

         + Notes - 
            Note that the function expects the arguments_list parameter have the first argument
            from sys.argv, most commomly the filename of the script, trimmed off (this can be 
            done by `del arguments_list.arguments_list[0]`. 
        """
        self.module = 'help'
        self.exit_code = 0
        self.arguments = arguments_list

        if len(self.arguments.arguments_list) > 0:
            self.module = self.arguments.arguments_list[0]
            del self.arguments.arguments_list[0]

        self.logger = Logger(self.arguments.log_level)
        return

    def run_module(self) -> None:
        """Runs the module and cleanup/catches any errors it emits

         + Notes - 
            The `run_module` method does not return the exit code of the module it runs. It simply
            stores the exit code in a class member variable (`self.exit_code`), which can be later
            accessed. 

            Additionally, this method should also not throw any exceptions
        """
        try:
            if self.module == 'help':
                help.run_module(self.arguments)
            if self.module == 'version':
                version.run_module(self.arguments)
            if self.module == 'presets':
                presets.run_module(self.arguments)
            if self.module == 'convert':
                convert.run_module(self.arguments)
            if self.module not in AvailableModules:
                raise ArgumentParseError(self.module)
        except ArgumentParseError as error:
            self.logger.log(f'[red][Fatal] ArgumentParseError: inapt argument \'{error.argument}\'', level=4)
            self.exit_code = 64
        except ArgumentValidationError as error:
            self.logger.log(f'[red][Fatal] ArgumentParseError: {error.message}', level=4)
            self.exit_code = 64
        except BaseError as error:
            self.logger.log(f'[red][Fatal] BaseError: An unknown fatal error has occured', level=4)
            self.exit_code = error.code
        return
