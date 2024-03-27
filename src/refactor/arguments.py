"""Arguments related classes and exceptions"""

available_modules = ["help", "version", "preset", "convert"]


class ArgumentBase:
    """A list of available arguments that the program accepts"""


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
