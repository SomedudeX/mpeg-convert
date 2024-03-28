from ..utils import Logger
from ..arguments import ArgumentBase


class HelpArguments(ArgumentBase):

    def __init__(
        self,
        arguments: ArgumentBase
    ) -> None:
        ...


def run_module(args: ArgumentBase):
    log = Logger(args.log_level)
    log.info(f'Running module help')
    log.info(f'Received arguments: {args.arguments_list}')
    log.warning(f'Module help unimplemented')
    ...
