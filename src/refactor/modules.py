"""The central hub for launching, managing, and closing modules"""

from . import arguments
from . import utils


class ModulesManager:
    """Manages launching, running, and closing modules"""
    
    def __init__(
        self,
        args: list[str],
    ) -> None:
        """Initializes a ModulesManager object

         + Args - 
            args: The list of arguments to pass to the module (most likely sys.argv)"""
        self.exit_code = 0
        self.arguments = args
        self.module = args[1]

        if self.module not in arguments.available_modules:
            raise arguments.ArgumentValidationError(f"{self.module} is not a valid module")

        self.logger = utils.Logger("modules.py")
        self.logger.log("[Debug] Succesfully initialied ModulesManager")
        return

    def run_module(self) -> None:
        """Runs the module and cleanup/catches any errors it emits"""
        ...
