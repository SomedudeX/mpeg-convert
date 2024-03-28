from ..utils import Logger
from ..arguments import ArgumentBase


class ConvertArguments(ArgumentBase):

    def __init__(
        self,
        arguments: ArgumentBase
    ) -> None:
        ...


def run_module(args: ArgumentBase):
    console = Logger(args.log_level)
    console.log(f'[Info] Running module convert', level=2)
    console.log(f'[Info] Received arguments: {args.arguments_list}', level=2)
    console.log(f'[yellow][Warning] Module convert unimplemented', level=3)
    ...
