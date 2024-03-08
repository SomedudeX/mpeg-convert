"""Anything related to command-line arguments"""

from .modules import presets


class ArgumentParseError(Exception):
    """An error emitted when an unexpected argument is encountered"""
    
    def __init__(
        self,
        argument: str
    ) -> None:
        """Initializes an instance of ArgumentParseError"""
        self.arguments = argument
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


class ArgumentBase:
    """A list of available arguments that the program accepts"""
    
    def __init__(self) -> None:
        """Initializes an interance of ArgumentsBase with default arguments"""
        self.help = False
        self.version = False
        self.verbose = False
        self.make_preset = False
        self.list_preset = False
        self.dump_preset = False
        
        self.input_file = ""
        self.output_file = ""
        
        self.selected_preset = "__interactive__"
        return


class ArgumentsHandler:
    """Handles command-line arguments inputted by the user"""
    
    def __init__(
        self, 
        arguments: list[str]
    ) -> None: 
        """Initializes an instance of ArgumentsHandler as well as a copy of 
        the default arguments
        
        + Args - 
            arguments: The list of arguments from sys.argv
        """
        self.processed_args = ArgumentBase()
        
        self.unprocessed_args = arguments
        self.unprocessed_args.pop(0)
        
        self.available_presets = [command.internal_value for command in presets.load_presets()]
        self.arguments_len = len(arguments)
        return
        
    def process_args(self) -> ArgumentBase:
        """Processes the command-line arguments into ArgumentsBase
        
        + Notes -
            When an unexpected argument is encountered, this method will
            throw an ArgumentsError. Optional flags can be interlaced with
            required positionals in arguments; if multiple preset flags are 
            specified, only the last flag is considered. 
        """
        
        if self.arguments_len == 0:
            self.processed_args.help = True
            return self.processed_args
        
        for argument in self.unprocessed_args:
            if self.map_optionals(argument):
                continue
            if self.map_required(argument):
                continue
        
        return self.processed_args
    
    def map_optionals(
        self, 
        argument: str
    ) -> bool:
        """Maps optioinal command-line flags to internal ArgumentsBase"""
        if argument in self.available_presets:
            self.processed_args.selected_preset = argument
            return True
        if argument == "--preset-make":
            self.processed_args.make_preset = True
            return True
        if argument == "--preset-list":
            self.processed_args.list_preset = True
            return True
        if argument == "--preset-dump":
            self.processed_args.dump_preset = True
            return True
        if argument == "--version":
            self.processed_args.version = True
            return True
        if argument == "-v" or argument == "--verbose":
            self.processed_args.verbose = True
            return True
        if argument == "-h" or argument == "--help":
            self.processed_args.help = True
            return True
        if not argument[0] == "-":
            return False
        raise ArgumentParseError(argument)
        
    def map_required(
        self,
        argument: str
    ) -> bool:
        """Maps required positionals to ArgumentsBase"""
        if self.processed_args.input_file == "":
            self.processed_args.input_file = argument
            return True
        if self.processed_args.output_file == "":
            self.processed_args.output_file = argument
            return True
        raise ArgumentParseError(argument)
