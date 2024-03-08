import json

from .. import utils


class Preset:
    
    def __init__(
        self,
        name: str,
        command: str
    ) -> None:
        self.name = name
        self.command = command
        self.internal_value = "--" + name
        return


def load_presets() -> list[Preset]:
    ret = []
    utils.create_json("convert_presets.json")
    with open("convert_presets.json", "r") as file:
        presets = json.load(file)
    for current_preset in presets:
        current_name = current_preset["name"]
        current_command = current_preset["command"]
        ret.append(Preset(current_name, current_command))
    return ret
