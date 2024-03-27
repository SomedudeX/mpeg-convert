from .. import arguments


class ConvertArguments(arguments.ArgumentBase):

    def __init__(
        self,
        arguments: arguments.ArgumentBase
    ) -> None:
        ...


def run_module(args: arguments.ArgumentBase):
    ...
