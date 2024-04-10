from typing import List, Tuple, Dict, Any

AvailableModules = ["", "help", "version", "console", "interactive"]


class ArgumentsError(Exception):
    """An ArgumentsError should be thrown when there is an error parsing an
    argument or there is an error in an argument.
    """
    def __init__(
        self,
        message: str,
        code: int = 1
    ) -> None:
        """Initializes an ArgumentsError instance"""
        self.message = message
        self.code = code
        super().__init__()


def is_flag(arg: str) -> bool:
    """Whether an argument is a flag"""
    assert len(arg) > 0
    return arg[0] == "-"


def is_int(arg: str) -> bool:
    """Whether a string can be converted to an integer"""
    if not isinstance(arg, str):
        return False
    return arg.isdigit()


def is_stacked_flag(flag: str) -> bool:
    """Whether a flag is stacked (e.g. `ls -la` is a stacked flag)"""
    if len(flag) <= 2:
        return False
    return flag[0] == "-" and flag[1] != "-"


def process_bool_flag(flag: tuple) -> int | str:
    """Attempts to convert an integer flag into a boolean"""
    if not is_int(flag[1]):
        return flag[1]
    return bool(int(flag[1]))


def split_arguments(argv: List[str]) -> Tuple[Any, Any]:
    """Splits sys.argv into parsable lists. Returns a tuple"""
    for index, arg in enumerate(argv):
        if is_flag(arg):
            flags = argv[index:]
            positionals = argv[:index]
            return positionals, split_flags(flags)
    return argv, []


def split_flags(flags: List[str]) -> List[Tuple]:
    """Splits the flags into a list of tuples such that for each tuple in the
    list, the first index will be the raw command-line argument and the second
    index will contain the specified value. For boolean flags, the value will
    default to `True` if not specified
    """
    ret = []
    for _ in range(len(flags)):
        if len(flags) == 0:
            break
        current_flag = flags[0]
        if "=" in current_flag:
            option = current_flag.split("=")[0]
            value = current_flag.split("=")[1]
            ret.append((option, value))
            del flags[0]
            continue
        elif len(flags) == 1 or flags[1][0] == "-":
            option = current_flag
            value = True
            ret.append((option, value))
            del flags[0]
            continue
        elif current_flag[0] == "-":
            option = current_flag
            value = flags[1]
            ret.append((option, value))
            del flags[0], flags[0]
            continue
        raise ArgumentsError(f"error parsing '{current_flag}' (unexpected trailing positional)", 1)
    return ret


def validate_argument_type(arguments: Dict[str, str]) -> None:
    """Validate the type of the arguments given by the user

    Parameters:
        arguments: The arguments to validate
    """
    if not isinstance(arguments["preset"], str):
        raise ArgumentsError(f"expected a string for argument '--preset', got '{arguments['preset']}' instead", 1)
    if not isinstance(arguments["debug"], bool):
        raise ArgumentsError(f"expected a boolean for argument '--debug', got '{arguments['debug']}' instead", 1)
    if not isinstance(arguments["quiet"], bool):
        raise ArgumentsError(f"expected a boolean for argument '--quiet', got '{arguments['quiet']}' instead", 1)
    if arguments["quiet"] and arguments["debug"]:
        raise ArgumentsError(f"flags '--debug' and '--quiet' cannot be both specified", 1)
    return


def parse_arguments(argv: List[str]) -> Dict[str, Any]:
    """Parse command-line arguments obtained from sys.argv
    
    Returns:
        A dictionary containing the various different available commands and
        flags that mpeg-convert accepts. 
        
    Notes: 
        The "module" key of the returned value corresponds to the module to
        activate. The reason it is a list is that there may be submodules, in
        which case it would be handled separately by the modules themselves. 
        For example, the command `mpeg-convert help interactive` would yield
        the following list of modules and submodules: 
            ['help', 'interactive']
        
        If any further options are to be added to any module, make sure to add
        the flags here.
    """
    ret = {
        "module": [""],
        "preset": "",
        "debug": False,
        "quiet": False
    }

    positionals, flags = split_arguments(argv)
    
    if len(positionals) > 0:
        ret["module"] = positionals

    for flag in flags:   # Mapping each command line flag to a dictionary key
        if flag[0] == "--debug" or flag[0] == "-d":
            ret["debug"] = process_bool_flag(flags[0])
            continue
        if flag[0] == "--quiet" or flag[0] == "-q":
            ret["quiet"] = process_bool_flag(flags[0])
            continue
        if flag[0] == "--preset":
            ret["preset"] = flag[1]
            continue
        if flag[0] == "--input":
            ret["input"] = flag[1]
            continue
        if flag[0] == "--output":
            ret["output"] = flag[1]
            continue
        if is_stacked_flag(flag[0]):
            raise ArgumentsError(f"stacked flag '{flag[0]}' not allowed", 1)
        raise ArgumentsError(f"invalid flag '{flag[0]}' received", 1)
    return ret
