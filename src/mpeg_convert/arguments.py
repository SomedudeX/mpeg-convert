AvailableModules = ["", "help", "version", "console", "interactive"]


class ProgramArguments:
    module = ""
    flag_end_index = -1
    flag_start_index = -1


def parse_arguments(argv: list[str]) -> ProgramArguments:
    ret = ProgramArguments()
    if len(argv) == 1:
        ret.module = ""
    if len(argv) > 1:
        ret.module = argv[1]
    return ret
