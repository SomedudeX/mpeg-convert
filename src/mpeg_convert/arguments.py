from typing import Any, Dict, List, Union, Tuple
from .exceptions import ArgumentsError


class ArgumentFlag:
    """A flag encountered during the parsing of arguments"""
    def __init__(
        self,
        argument: Any,
        value: Any
    ) -> None:
        """Initializes an instance of ArgumentFlag"""
        self.arg = argument
        self.val = value
        return


def is_flag(arg: str) -> bool:
    """Whether a string is a flag"""
    return len(arg) >= 1 and \
           arg[0] == "-"


def is_int(arg: str) -> bool:
    """Whether a string is an integer"""
    return isinstance(arg, str) and \
           len(arg) >= 1 and \
           arg.isdigit()


def process_bool_flag(value: str) -> Union[int, str]:
    """Attempts to convert an integer flag into a boolean"""
    if not is_int(value):
        return value
    return bool(int(value))


def is_stacked_flag(flag: str) -> bool:
    """Whether an argument is a stacked flag (e.g. -abc)"""
    return len(flag) >= 2 and \
           flag[0] == "-" and \
           flag[1] != "-"


def split_arguments(argv: List[str]) -> Tuple[List[str], List[ArgumentFlag]]:
    """Splits sys.argv into parsable lists. Returns a tuple"""
    for index, argument in enumerate(argv):
        if is_flag(argument):
            flags = argv[index:]
            positionals = argv[:index]
            return positionals, split_flags(flags)
    return argv, []


def split_flags(flags: List[str]) -> List[ArgumentFlag]:
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
            ret.append(ArgumentFlag(option, value))
            del flags[0]
            continue
        elif len(flags) == 1 or flags[1][0] == "-":
            option = current_flag
            value = True
            ret.append(ArgumentFlag(option, value))
            del flags[0]
            continue
        elif current_flag[0] == "-":
            option = current_flag
            value = flags[1]
            ret.append(ArgumentFlag(option, value))
            del flags[0], flags[0]
            continue
        raise ArgumentsError(
            f"error parsing '{current_flag}'" + 
            "(unexpected trailing positional)", code=1)
    return ret


def parse_arguments(argv: List[str]) -> Dict[str, Any]:
    """Parse the arguments from sys.argv into a dictionary"""
    positionals, flags = split_arguments(argv[1:])
    parsed_arguments = {
        "module": [""],
        "output": False,
        "input": False,
        "debug": False
    }

    if len(positionals) > 0:
        parsed_arguments["module"] = positionals

    for flag in flags:   # Mapping each command line flag to a dictionary key
        if flag.arg == "--output" or flag.arg == "-o":
            parsed_arguments["output"] = flag.val
            continue
        if flag.arg == "--input" or flag.arg == "-i":
            parsed_arguments["input"] = flag.val
            continue
        if flag.arg == "--debug" or flag.arg == "-d":
            parsed_arguments["debug"] = process_bool_flag(flag.val)
            continue
        if is_stacked_flag(flag.arg):
            raise ArgumentsError(f"stacked flag '{flag.arg}' not allowed", code=1)
        raise ArgumentsError(f"invalid flag '{flag.arg}' received", code=1)
    return parsed_arguments