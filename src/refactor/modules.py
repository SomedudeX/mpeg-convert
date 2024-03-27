"""The central hub for launching, managing, and closing modules"""

from . import utils
from . import arguments

from .core import help
from .core import version
from .core import convert
from .core import presets


class ModulesManager:
    """Manages launching, running, and closing modules"""
    
    def __init__(
        self,
        arguments_list: list[str],
    ) -> None:
        """Initializes a ModulesManager object

         + Args - 
            args: The list of arguments to pass to the module (most likely sys.argv)"""
        self.exit_code = 0
        self.arguments = arguments.ArgumentBase()
        self.arguments.scan_flags(arguments_list)

        self.module = 'help'
        if len(arguments_list) > 1:
            self.module = arguments_list[1]
        if self.module not in arguments.available_modules:
            raise arguments.ArgumentValidationError(f'\'{self.module}\' is not a valid argument')

        self.logger = utils.Logger(self.arguments.log_level)
        return

    def run_module(self) -> None:
        """Runs the module and cleanup/catches any errors it emits"""
        try:
            if self.module == 'help':
                help.run_module(self.arguments)
            if self.module == 'version':
                version.run_module(self.arguments)
            if self.module == 'presets':
                presets.run_module(self.arguments)
            if self.module == 'convert':
                convert.run_module(self.arguments)
        except Exception:
            self.logger.log('Exception')
            self.exit_code = 255
        return
