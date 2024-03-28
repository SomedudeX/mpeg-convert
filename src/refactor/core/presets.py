from ..utils import Logger
from ..arguments import ArgumentBase


class PresetsArguments(ArgumentBase):

    def __init__(
        self,
        arguments: ArgumentBase
    ) -> None:
        ...


def run_module(args: ArgumentBase):
    log = Logger(args.log_level)
    log.info(f'Running module presets')
    log.info(f'Received arguments: {args.arguments_list}')
    log.warning(f'Module presets unimplemented')
    ...


# """Anything related to FFmpeg presets"""
# import json
#
# from .. import utils
#
#
# class Preset:
#     """An internal representation of a preset"""
#     def __init__(
#         self,
#         name: str,
#         command: str
#     ) -> None:
#         """Initialize an instance of Preset"""
#         self.name = name
#         self.command = command
#         return

# def load_presets() -> list[Preset]:
#     """Load presets into a list to represent them internally"""
#     ret = []
#     utils.create_json("convert_presets.json")
#     with open("convert_presets.json", "r") as file:
#         presets = json.load(file)
#     for current_preset in presets:
#         current_name = current_preset["name"]
#         current_command = current_preset["command"]
#         ret.append(Preset(current_name, current_command))
#     return ret
