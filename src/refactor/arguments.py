"""Arguments related classes and exceptions"""

available_modules = ['help', 'version', 'preset', 'convert']


class ArgumentBase:
    """The basic list of arguments and flags that the user inputted"""

    def __init__(
        self,
        module: str,
        log_level: int
    ) -> None:
        """Initializes an instance of ArgumentBase"""
        self.module = module
        self.log_level = log_level
        return


class ArgumentParseError(Exception):
    """An error emitted when an unexpected argument is encountered"""
    
    def __init__(
        self,
        argument: str
    ) -> None:
        """Initializes an instance of ArgumentParseError"""
        self.argument = argument
        return
        
        
class ArgumentValidationError(Exception):
    """An error emitted when an argument is invalid"""
    
    def __init__(
        self,
        message: str
    ) -> None:
        """Initializes an instance of ArgumentValidationError"""
        self.message = message
        return
