from typing import List, Tuple, Any

from .exceptions import ArgumentsError

AvailableModules = ["", "help", "version", "console", "interactive"]


def is_flag(arg: str) -> bool:
    """Whether an argument is a flag"""
    assert(len(arg) > 0)
    return arg[0] == "-"


def is_stacked_flag(flag: str) -> bool:
    """Whether a flag is stacked (e.g. `ls -la`)"""
    if len(flag) <= 2:
        return False
    return flag[0] == "-" and flag[1] != "-"


def split_arguments(argv: List[str]) -> Tuple[Any, Any]:
    """Splits sys.argv into parsable lists. Returns a tuple"""
    for index, arg in enumerate(argv):
        if is_flag(arg):
            flags = argv[index:]
            positionals = argv[:index]
            return positionals, split_flags(flags)
    return argv, []


def split_flags(flags: List[str]) -> List[Tuple[str, str | bool]]:
    """Splits the flags into a list of tuples such that for each tuple in the
    list, the first index will be the raw command-line argument and the second
    index will contain the specified value. For boolean flags, the value will
    default to `True` if not specified
    """
    ret = []
    for _ in range(len(flags)):
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
            del flags[0], flags[1]
            continue
        raise ArgumentsError(f"error parsing '{current_flag}' (unexpected trailing positional)")
    return ret


def parse_arguments(argv: List[str]) -> dict:
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
    ret = {}
    ret["module"] = [""]    # Defaults
    ret["preset"] = ""
    ret["debug"] = False
    ret["quiet"] = False

    positionals, flags = split_arguments(argv)
    
    if len(positionals) > 0:
        ret["module"] = positionals

    for flag in flags:   # Mapping each command line flag to a dictionary key
        if flag[0] == "--debug" or flag[0] == "-d":
            ret["debug"] = flag[1]
            continue
        if flag[0] == "--quiet" or flag[0] == "-q":
            ret["quiet"] = flag[1]
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
            raise ArgumentsError(f"stacked flag '{flag[0]}' not allowed")
        raise ArgumentsError(f"invalid flag '{flag[0]}' received")
    return ret
