"""Arguments related classes and exceptions"""

from . import exceptions

available_modules = ['help', 'version', 'preset', 'convert']


class ArgumentBase:
    """A list of arguments"""

    def __init__(self) -> None:
        """Initializes an instance of ArgumentBase; should only be used when
        parsing module-independent flags at the start of the execution of the
        program"""
        self.log_level = 2
        self.quiet = False
        self.debug = False
        return

    def scan_flags(
        self,
        arguments_list: list[str]
    ) -> None:
        """Adds basic arguments to instance

         + Args - 
            arguments_list: The list of arguments obtained usually from sys.argv
        """
        for i in range(len(arguments_list) - 1, 0):
            if arguments_list[i][0] != '-':
                break
            if arguments_list[i] == '--quiet':
                self.quiet = True
                del arguments_list[i]
            if arguments_list[i] == '--debug':
                self.debug = True
                del arguments_list[i]
        return


class ArgumentParseError(exceptions.BaseError):
    """An error emitted when an unexpected argument is encountered"""
    
    def __init__(
        self,
        argument: str,
        code: int = 64
    ) -> None:
        """Initializes an instance of ArgumentParseError

         + Args - 
            argument: The argument that caused the parse error
            code: The exit code that the program should terminate with
        """
        self.argument = argument
        super().__init__(code)
        return
        
        
class ArgumentValidationError(exceptions.BaseError):
    """An error emitted when an argument is invalid"""
    
    def __init__(
        self,
        message: str,
        code: int = 64
    ) -> None:
        """Initializes an instance of ArgumentValidationError

         + Args - 
            message: A short message about the validation error
            code: The exit code that the program should terminate with
        """
        self.message = message
        super().__init__(code)
        return
