"""Arguments related classes and exceptions"""

from .exceptions import BaseError

AvailableModules = ['help', 'version', 'preset', 'convert']


class ArgumentParseError(BaseError):
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
        
        
class ArgumentValidationError(BaseError):
    """An error emitted when there are conflicting arguments present"""
    
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


class ArgumentBase:
    """A list of arguments that the program accepts"""

    def __init__(
        self,
        arguments_list: list[str]
    ) -> None:
        """Initializes an instance of ArgumentBase

         + Args - 
            arguments_list: A list of arguments (most likely from sys.argv)

         + Notes - 
            Should only be used when parsing module-independent flags at the 
            start of the execution of the program. Otherwise, this class should 
            be customized through inheritance for each individual modules.

            Additionally, when adding new flags to the tool, initialize the 
            flag variable here but scan for the flag (if changed) in a
            separate function. This is to keep the __init__ function clean. 
        """
        self.arguments_list = arguments_list

        self.log_level = 2              # level 2 (info) is the default log level
        self.determine_log_flag()
        return

    def determine_log_flag(self) -> None:
        """Scans argument flag for log level changes from last to first"""
        _debug, _quiet = False, False
        for i in range(len(self.arguments_list) - 1, 0, -1):
            if self.arguments_list[i][0] != '-':
                break
            if self.arguments_list[i] == '--quiet':
                _quiet = True
                del self.arguments_list[i]
                continue
            if self.arguments_list[i] == '--debug':
                _debug = True
                del self.arguments_list[i]
                continue

        if _debug:
            self.log_level = 1
        if _quiet:
            self.log_level = 3
        if _quiet and _debug:
            raise ArgumentValidationError('cannot have both \'--quiet\' and \'--debug\' flags')
        return
        
