"""Arguments related classes and exceptions"""

available_modules = ['help', 'version', 'preset', 'convert']


class ArgumentBase:
    """The basic list of arguments and flags that the user inputted"""

    def __init__(self) -> None:
        """Initializes an instance of ArgumentBase"""
        self.module = 'help'
        self.log_level = 2      # Log all info and fatal
        return

    def add_arguments(
        self,
        arguments_list: list[str]
    ) -> None:
        """Adds basic arguments to instance

         + Args - 
            arguments_list: The list of arguments obtained usually from sys.argv
        """
        if len(arguments_list) > 1:
            self.module = arguments_list[1]
        if '--verbose' in arguments_list:
            self.log_level = 1  # Log all debug, info, and fatal
        return


class ArgumentParseError(Exception):
    """An error emitted when an unexpected argument is encountered"""
    
    def __init__(
        self,
        argument: str
    ) -> None:
        """Initializes an instance of ArgumentParseError

         + Args - 
            argument: The argument that caused the parse error
        """
        self.argument = argument
        return
        
        
class ArgumentValidationError(Exception):
    """An error emitted when an argument is invalid"""
    
    def __init__(
        self,
        message: str
    ) -> None:
        """Initializes an instance of ArgumentValidationError

         + Args - 
            message: A short message about the validation error"""
        self.message = message
        return
