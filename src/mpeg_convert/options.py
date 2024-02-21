"""Handles the process of asking user conversion options"""
import os

from rich.console import Console
from rich.prompt import Prompt, Confirm

from mpeg_convert.customization import *


class OptionsHandler:
    """The OptionsHandler() class asks the user questions on how to transcode the file"""

    def __init__(
            self,
            _metadata: dict,
            _audio_stream: int,
            _video_stream: int,
            _filepath_out: str
    ) -> None:
        """Initializes an instance of OptionsHandler()
        
        + Notes - 
            The _metadata is used only for obtaining information regarding
            the audio channels. 
        
        + Args - 
            _metadata: a dictionary representing the metadata from FFprobe
            _audio_stream: the first audio stream
            _video_stream: the first video stream
        """
        self.console = Console(highlight=False)
        self.error_console = Console(style="red", highlight=False)

        self.options = {}
        self.metadata = _metadata
        self.audio_stream = _audio_stream
        self.video_stream = _video_stream

        self._output = _filepath_out
        self.replace = "n"

    def ask_encode_options(
            self,
            _default: dict = {}
    ) -> dict[str, str]:
        """Asks the user for encoding options
        
        + Notes -
            Tries to conform to the user's request as much as possible, 
            however in the event that an audio/video stream cannot be 
            discovered, the ask...() function automatically aborts. 
            
            This may lead to unexpected issues. 
            
            Additionally, the custom options are an experimental option, 
            meaning that they are not tested well and may lead to issues. 
        
        + Args -
            _default: whether to use the default options
            
        + Returns -
            Dictionary: representing the commands that matches the user's 
            request. The keys of the dictionary corresponds to the option,
            and the values of the dictionary corresponds to the value in 
            ffmpeg. The options are stripped of the dash (-) in front
            
            e.g. { 'c:a': 'libmp3lame' } corresponds to '-c:a libmp3lame' 
        """
        if _default != {}:
            if os.path.isfile(self._output):
                self.console.print()
                self.replace = Prompt.ask(
                    " >  Replace existing output path",
                    choices=["y", "n"],
                    default="n"
                )

                if self.replace == "n":
                    self.console.print()
                    self.console.log("[Info] Finished gathering encoding options")
                    self.console.log("[Info] User declined operation, terminating")
                    raise SystemExit(0)
            
            return _default

        self.console.print()
        self.console.print(" >  Encode for...")
        self.console.print("[1] Audio only")
        self.console.print("[2] Video only")
        self.console.print("[3] Video and audio (default)")
        self.console.print("[4] Skip encode options")
        _encode = Prompt.ask(
            " >  Select an option",
            choices=["1", "2", "3", "4"],
            default="3"
        )

        self.options: dict = {}
        if _encode == "1":
            self.options = self._ask_audio_options()
            self.options["vn"] = None
        if _encode == "2":
            self.options = self._ask_video_options()
            self.options["an"] = None
        if _encode == "3":
            self.options = (self._ask_video_options() |
                            self._ask_audio_options())

        self.console.print()
        self.console.print("[bold] -*- Miscellaneous options -*-")

        if os.path.isfile(self._output):
            self.console.print()
            self.replace = Prompt.ask(
                " >  Replace existing output path",
                choices=["y", "n"],
                default="n"
            )

            if self.replace == "n":
                self.console.print()
                self.console.log("[Info] Finished gathering encoding options")
                self.console.log("[Info] User declined operation, terminating")
                raise SystemExit(0)

        self.console.print()
        _metadata_strip = Prompt.ask(
            " >  Enable file metadata stripping",
            choices=["y", "n"],
            default="y"
        )

        self.console.print()
        _additional_commands = Prompt.ask(
            " >  Custom options to ffmpeg ('-option value -option2 value...')\n" +
            " >  Use empty field to skip"
        )

        if _metadata_strip == "y":
            self.options["map_metadata"] = "-1"
        if _metadata_strip == "n":
            self.options["map_metadata"] = "0"

        self.options = self.options | self._parse_custom_command(_additional_commands)

        self.console.print()
        return self.options

    def _ask_audio_options(self) -> dict:
        """Asks the user for audio encoding options
        
        + Notes - 
            If no audio streams are discovered, asks the user if
            they would like to proceed. 
            
        + Returns -
            Dictionary: containing the arguments to pass to FFmpeg. 
        """

        _ret: dict = {}

        if self.audio_stream == -1:
            self.error_console.print()
            self.error_console.print("[Error] No audio stream detected in metadata! ")
            self.error_console.print(" - This may lead to unexpected issues")
            self.error_console.print(" - You are entering unknown territory")
            _continue = Confirm.ask("[red] - Would you like to continue?")
            if not _continue:
                return _ret

        self.console.print()
        self.console.print("[bold] -*- Audio options -*-")
        for _index, _question in enumerate(AUDIO_OPTIONS):
            try:
                _ret = _ret | self._ask_question(_question)
            except KeyError as e: 
                self.error_console.print()
                self.error_console.log(f"[Error] Audio question {_index + 1} has invalid key {e}")
                self.error_console.log(f"- Use the '--customize' flag to see the error")
                self.error_console.log(f"- Mpeg-convert may not function currectly")
                self.error_console.log(f"- Skipping to the next audio question")
            except ValueError as e:
                self.error_console.print()
                self.error_console.log(f"[Error] Audio question {_index + 1} has invalid option(s)")
                self.error_console.log(f"- Use the '--customize' flag to see the error")
                self.error_console.log(f"- Mpeg-convert may not function currectly")
                self.error_console.log(f"- Skipping to the next audio question")
            except IndexError as e:
                self.error_console.print()
                self.error_console.log(f"[Error] Audio question {_index + 1} has invalid option(s)")
                self.error_console.log(f"- Use the '--customize' flag to see the error")
                self.error_console.log(f"- Mpeg-convert may not function currectly")
                self.error_console.log(f"- Skipping to the next audio question")

        return _ret

    def _ask_video_options(self) -> dict:
        """Asks the user for video encoding options
        
        + Notes - 
            If no video streams are discovered, asks the user if
            they would like to proceed. 
            
        + Returns -
            Dictionary: containing the arguments to pass to FFmpeg. 
        """
        _ret: dict = {}

        if self.video_stream == -1:
            self.error_console.print()
            self.error_console.print("[Error] No video stream detected in metadata! ")
            self.error_console.print(" - This may lead to unexpected issues")
            self.error_console.print(" - You are entering unknown territory")
            _continue = Confirm.ask("[red] - Would you like to continue?")
            if not _continue:
                return _ret

        self.console.print()
        self.console.print("[bold] -*- Video options -*-")
        for _index, _question in enumerate(VIDEO_OPTIONS):
            try:
                _ret = _ret | self._ask_question(_question)
            except KeyError as e: 
                self.error_console.print()
                self.error_console.log(f"[Error] Video question {_index + 1} has invalid key {e}")
                self.error_console.log(f"- Use the '--customize' flag to see the error")
                self.error_console.log(f"- Mpeg-convert may not function currectly")
                self.error_console.log(f"- Skipping to the next video question")
            except ValueError as e:
                self.error_console.print()
                self.error_console.log(f"[Error] Audio question {_index + 1} has invalid option(s)")
                self.error_console.log(f"- Use the '--customize' flag to see the error")
                self.error_console.log(f"- Mpeg-convert may not function currectly")
                self.error_console.log(f"- Skipping to the next video question")
            except IndexError as e:
                self.error_console.print()
                self.error_console.log(f"[Error] Audio question {_index + 1} has invalid option(s)")
                self.error_console.log(f"- Use the '--customize' flag to see the error")
                self.error_console.log(f"- Mpeg-convert may not function currectly")
                self.error_console.log(f"- Skipping to the next video question")

        return _ret

    def _ask_question(
            self,
            _question: dict
    ) -> dict:
        """Asks the user a question
        
        + Args -
            Question: a dictionary input of the different properties of the question
            
        + Returns -
            Dictionary: containing the option (key) and the user's input (value)
        """
        _ret: dict = {}

        if _question["option"][0] == "-":                   # The python-ffmpeg api inserts a dash (-) symbol
            _question["option"] = _question["option"][1:]   # for you, so we have to get rid of the dash.
        
        if _question["type"] == "choice":
            _custom_index = len(_question["choices"]) + 0
            _none_index = len(_question["choices"]) + 1
            _total_length = len(_question["choices"]) + 2

            self.console.print()
            self.console.print(" > ", _question["title"])
            self._print_choices(
                _question["choices"],
                _question["default"]
            )

            _answer_index = Prompt.ask(
                " >  Select an option",
                choices=[str(i + 1) for i in range(_total_length)],
                default=str(_question["default"]),
            )

            _answer_index = int(_answer_index) - 1
            if _answer_index == _none_index:
                self.console.print(" >  Option removed from ffmpeg arguments")
                return _ret
            if _answer_index == _custom_index:
                _ret[_question["option"]] = Prompt.ask(" >  Custom value")
                return _ret

            _ret[_question["option"]] = _question["choices"][_answer_index][1]
            return _ret

        if _question["type"] == "input":
            self.console.print()
            _answer_index = Prompt.ask(
                " -  " + _question["title"]
            )

            _ret[_question["option"]] = _answer_index
            return _ret

        return _ret

    def _print_choices(
            self,
            _choices: list[tuple],
            _default: int
    ) -> None:
        """Prints the choices from a list of tuples
        
        + Args -
            Choices: a list of tuples containing the different options to display
            Default: The index to mark as 'default'
        """
        _custom_index = len(_choices) + 1
        _none_index = len(_choices) + 2

        for index, value in enumerate(_choices):
            _number = index + 1
            _line = value[0]
            _line = f"[{_number}] {_line}"
            if _default == index + 1:
                _line = _line + " (default)"
            self.console.print(_line)

        self.console.print(f"[{_custom_index}] Custom value")
        self.console.print(f"[{_none_index}] Remove option")
        return

    @staticmethod
    def _parse_custom_command(_commands: str) -> dict:
        """Parses the optional commands that the user enters into ffmpeg
        
        + Args -
            Commands: a string of commands that the user enters
        
        + Returns -
            Dictionary: a dictionary containing the options (keys) and the user's
            value (values)
            
        + Notes -
            This method is not extensively tested and is not guaranteed to work
            in all scenarios. Exercise caution when using the custom commands
        """
        _ret: dict = {}

        if _commands == "":
            return _ret

        _commands += " "
        _option: str = ""
        _value: str = ""
        _is_option: bool = True
        _current_str: str = ""

        for _ in range(len(_commands)):
            if len(_commands) == 0:
                break
            if _commands[0] == "-":
                _commands = _commands[1:]
                _is_option = True
                continue
            if _commands[0] == " " and _is_option == True:
                _is_option = False
                _option = _current_str
                _commands = _commands[1:]
                _current_str = ""
                _ret[_option] = None
                continue
            if _commands[0] == " " and _is_option == False:
                _is_option = True
                _value = _current_str
                _commands = _commands[1:]
                _current_str = ""
                _ret[_option] = _value
                continue

            _current_str += _commands[0]
            _commands = _commands[1:]
            continue

        return _ret
