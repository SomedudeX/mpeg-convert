#!/usr/bin/env python3

# This file uses the following styles for token names: 
#     PascalCase       Class name
#     camelCase        Variable or function/method name
#     _underscore      Variable/function should be used only in the scope
#                      it's declared in (and should not be modified by user)

import os
import sys
import json

from rich.prompt import IntPrompt

try:
	from ffmpeg import FFmpeg, FFmpegError, Progress

	from rich.progress import Progress as ProgressBar, TaskProgressColumn
	from rich.progress import TextColumn, BarColumn
	from rich.prompt import Confirm, Prompt
	from rich.console import Console
	from rich import traceback

except ModuleNotFoundError as e:
	print(f" [Fatal] {str(e).capitalize()}")
	print(f" - Make sure you install all required modules by using `pip` or `pip3`")
	raise SystemExit(-1)


class MediaManager():

	def __init__(self, inputPath: str) -> None:
		"""Initializes an instane of `MediaManager`

		Args:
			inputPath - the path of the media file that the object will represent
		"""
		self.console = Console(highlight = True)

		self.inputPath = inputPath
		self.getMetadata()

	def getMetadata(self) -> None:
		"""Gets the metadata of the media file that the object is currently representing

		Returns:
			None - instead, fetches the metadata into the class attribute `self.metadata`
		"""
		self.console.log("[Info] Probing file properties and metadata...")
		_ffprobe = FFmpeg(executable = "ffprobe").input(
				self.inputPath,
				print_format = 'json',
				show_streams = None
		)

		self.metadata: dict = json.loads(_ffprobe.execute())
		return

	def askEncodeOptions(self) -> None:
		"""Asks the user for encoding options

		Returns: 
			A dictionary containing the arguments to pass to FFmpeg
		"""
		self.console.print()
		self.console.print("[bold] -*- Encoding options -*-")
		self.console.print()
		self.console.print("Encode for...")
		self.console.print("[1] Audio only")
		self.console.print("[2] Video only")
		self.console.print("[3] Both (default)")
		_encode = Prompt.ask("Select an option", choices = ["1", "2", "3"], default = "3")

		self.options: dict = {}
		if _encode == "1": 
			self.options = self.askAudioOptions()
			self.options["vn"] = None
		if _encode == "2": 
			self.options = self.askVideoOptions()
			self.options["an"] = None
		if _encode == "3": 
			self.options = self.askVideoOptions() | self.askAudioOptions()

		self.console.log(f"[Debug] Finished asking encoding options")
		return

	def askAudioOptions(self) -> dict:
		"""Asks the user for audio encoding options

		Returns: 
			A dictionary containing the arguments to pass to FFmpeg
		"""
		_ret: dict = {}
		self.console.print()
		self.console.print("[bold] -*- Audio options -*-")
		self.console.print()
		self.console.print(f"Audio codec presets -")
		self.console.print(f"[1] AAC")
		self.console.print(f"[2] MP3 (default)")
		self.console.print(f"[3] ALAC")
		self.console.print(f"[4] FLAC")
		self.console.print(f"[5] Custom encoder")
		_codec = Prompt.ask("Select a codec", choices = ["1", "2", "3", "4", "5"], default = "2")
		_codec = self._parseCodecAudio(_codec)

		self.console.print()
		self.console.print(f"Audio samplerate presets -")
		self.console.print(f"[1] 16000hz")
		self.console.print(f"[2] 44100hz")
		self.console.print(f"[3] 48000hz (default)")
		self.console.print(f"[4] 96000hz")
		self.console.print(f"[5] Custom samplerate")
		_samplerate = Prompt.ask("Select a samplerate", choices = ["1", "2", "3", "4", "5"], default = "3")
		_samplerate = self._parseSamplerate(_samplerate)
		
		self.console.print()
		self.console.print(f"Audio bitrate presets -")
		self.console.print(f"[1] 96k")
		self.console.print(f"[2] 128k")
		self.console.print(f"[3] 192k (default)")
		self.console.print(f"[4] 320k")
		self.console.print(f"[5] Custom bitrate")
		_bitrate = Prompt.ask("Select a birate", choices = ["1", "2", "3", "4", "5"], default = "3")
		_bitrate = self._parseBitrate(_bitrate)

		_channels = self.metadata["streams"][1]["channels"]

		_ret["codec:a"] = _codec
		_ret["ar"] = _samplerate
		_ret["b:a"] = _bitrate
		_ret["ac"] = str(_channels)

		return _ret

	def askVideoOptions(self) -> dict:
		"""Asks the user for video encoding options

		Note:
			The CRF value is hard-coded

		Returns: 
			A dictionary containing the arguments to pass to FFmpeg
		"""
		_ret: dict = {}
		self.console.print()
		self.console.print("[bold]-*- Video options -*-")
		self.console.print()
		self.console.print(f"Video resolution presets -")
		self.console.print(f"[bold][[cyan]1[/cyan]][/bold] 1280x720", highlight = False)
		self.console.print(f"[bold][[cyan]2[/cyan]][/bold] 1920x1080 (default)", highlight = False)
		self.console.print(f"[bold][[cyan]3[/cyan]][/bold] 2560x1440", highlight = False)
		self.console.print(f"[bold][[cyan]4[/cyan]][/bold] 3840x2160", highlight = False)
		self.console.print(f"[5] Custom resolution")
		_resolution = Prompt.ask("Select a resolution", choices = ["1", "2", "3", "4", "5"], default = "2")
		_resolution = self._parseResolution(_resolution)

		self.console.print()
		self.console.print(f"Video framerate presets -")
		self.console.print(f"[1] 24fps (default)")
		self.console.print(f"[2] 30fps")
		self.console.print(f"[3] 50fps")
		self.console.print(f"[4] 60fps")
		self.console.print(f"[5] Custom framerate")
		_framerate = Prompt.ask("Select a framerate", choices = ["1", "2", "3", "4", "5"], default = "1")
		_framerate = self._parseFramerate(_framerate)

		self.console.print()
		self.console.print(f"Video codec presets -")
		self.console.print(f"[bold][[cyan]1[/cyan]][/bold] H.264", highlight = False)
		self.console.print(f"[bold][[cyan]2[/cyan]][/bold] H.265 (default)", highlight = False)
		self.console.print(f"[3] AV1")
		self.console.print(f"[4] VP9")
		self.console.print(f"[5] Custom codec")
		_codec = Prompt.ask("Select a codec", choices = ["1", "2", "3", "4", "5"], default = "2")
		_codec = self._parseCodecVideo(_codec)

		self.console.print()
		self.console.print(f"Video quality -")
		_doLossless = Confirm.ask("Enable lossless video (CRF = 0)")


		_ret["r"] = _framerate
		_ret["s"] = _resolution
		_ret["codec:v"] = _codec

		if _doLossless:
			_ret["crf"] = "0"
		else:
			_ret["crf"] = IntPrompt.ask("Enter a CRF value (0-51)")

		return _ret

	def getTotalSecs(self) -> int:
		"""Gets the total length (in seconds) of the current video file

		Note: 
			Assumes that `stream 0` is the one and only video stream in the media file

		Returns:
			An integer representing the length (in seconds) of the current video file
		"""
		_ret = self.metadata["streams"][0]["duration"]
		_ret = float(_ret)
		return int(_ret)

	def getFramerate(self) -> int:
		"""Gets the average framerate of the current video file

		Note: 
			Assumes that `stream 0` is the one and only video stream in the media file

		Returns:
			An integer representing the framerate of the current video file
		"""
		_ret = self.metadata["streams"][0]["avg_frame_rate"]
		_ret = _ret[:-2]
		return int(_ret)

	@staticmethod
	def _parseResolution(_resolution: str) -> str:
		if _resolution == "1": return "1280x720"
		if _resolution == "2": return "1920x1080"
		if _resolution == "3": return "2560x1440"
		if _resolution == "4": return "3840x2160"
		if _resolution == "5": return Prompt.ask("Enter custom resolution (e.g. 2160x1440)")
		return "1920x1080"

	@staticmethod
	def _parseCodecVideo(_codec: str) -> str:
		if _codec == "1": 
			if sys.platform == "darwin": return "h264_videotoolbox"
			else: return "libx264"
		if _codec == "2": 
			if sys.platform == "darwin": return "hevc_videotoolbox"
			else: return "libx265"
		if _codec == "3": return "libsvtav1"
		if _codec == "4": return "libvpx-vp9"
		if _codec == "5": return Prompt.ask("Enter custom video encoder (e.g. libwebp)")
		return "libx264"

	@staticmethod
	def _parseCodecAudio(_codec: str) -> str:
		if _codec == "1": return "aac"
		if _codec == "2": return "libmp3lame"
		if _codec == "3": return "alac"
		if _codec == "4": return "flac"
		if _codec == "5": return Prompt.ask("Enter custom audio encoder (e.g. libtwolame)")
		return "libx264"

	@staticmethod
	def _parseFramerate(_framerate: str) -> str:
		if _framerate == "1": return "24"
		if _framerate == "2": return "30"
		if _framerate == "3": return "50"
		if _framerate == "4": return "60"
		if _framerate == "5": return Prompt.ask("Enter custom framerate (e.g. 23.976)")
		return "24"

	@staticmethod
	def _parseSamplerate(_samplerate: str) -> str:
		if _samplerate == "1": return "16000"
		if _samplerate == "2": return "44100"
		if _samplerate == "3": return "48000"
		if _samplerate == "4": return "96000"
		if _samplerate == "5": return Prompt.ask("Enter custom samplerate (e.g. 22050)")
		return "48000"

	@staticmethod
	def _parseBitrate(_bitrate: str) -> str:
		if _bitrate == "1": return "96k"
		if _bitrate == "2": return "128k"
		if _bitrate == "3": return "192k"
		if _bitrate == "4": return "320k"
		if _bitrate == "5": return Prompt.ask("Enter custom bitrate (e.g. 160)")
		return "192k"


class Program():
	"""
	A media file converter using the ffmpeg engine. 

	Usage: mpeg-convert <filepath.in> <filepath.out>

	Options:
		-d   --debug       Enable debug mode to see FFmpeg logs

	This tool is a simple wrapper for the ffmpeg engine to make the
	conversion between different video/audio formats a little easier for
	the everyday user. This program is not, however, a complete
	replacement for ffmpeg in any way. For that purpose, you should look
	look into other software such as Handbrake or DaVinci Resolve. 

	Additionally, this tool has been hacked together in a couple of
	days, meaning that some of the finer details has not been fleshed
	out yet -- expect some rough corners during use. This tool also has
	not been tested or designed for multiple video/audio streams. 

	Custom encoders can be listed by `ffmpeg -codecs`
	"""

	def __init__(self) -> None:
		"""Initializes an instance of `Program`"""
		self.console = Console()
		self.errorConsole = Console(stderr = True, style = "bold red")
		self.debug = False

		self.checkFFmpeg()

	def parseArgs(self) -> None:
		"""Parses the command-line arguments from the user"""
		_argv: list = sys.argv
		del _argv[0]

		_argc: int = len(_argv)

		if _argc == 0 or _argc == 1:
			self.console.print(self.__doc__, highlight = False)
			raise SystemExit(0)

		if _argc == 2:
			self.input = sys.argv[0]
			self.output = sys.argv[1]
			self.console.log(f"[Info] Raw command-line arguments: '{self.input}' and '{self.output}'")
			_cwd = os.getcwd() + "/"

			if self.input[0] != "/" and self.input[0] != "~":
				self.input = _cwd + self.input
			if self.output[0] != "/" and self.output[0] != "~":
				self.output = _cwd + self.output
			return

		if _argc == 3:
			self.debug = self.checkDebug(_argc, _argv)[0]
			if not self.debug: 
				self.errorConsole.log(f"[Fatal] parseArgs() failed: 3 arguments were provided but none of them are -d or --debug")
				raise SystemExit(1)

			self.console.log(f"[yellow][Info] Debug mode enabled: will output all FFmpeg logs")
			del _argv[self.checkDebug(_argc, _argv)[1]]
			self.input = sys.argv[0]
			self.output = sys.argv[1]
			self.console.log(f"[Info] Raw command-line arguments: '{self.input}' and '{self.output}'")
			_cwd = os.getcwd() + "/"

			if self.input[0] != "/" and self.input[0] != "~":
				self.input = _cwd + self.input
			if self.output[0] != "/" and self.output[0] != "~":
				self.output = _cwd + self.output
			return

		if _argc > 3:
			_args = ""
			for _arg in _argv:
				_args = _args + _arg + ", "
			_args = _args[:-2]
			self.errorConsole.log(f"[Fatal] parseArgs() failed: too many arguments were provided to the program ({_argc} received):")
			self.errorConsole.log(f" - Arguments: {_args}")
			raise SystemExit(1)

	@staticmethod
	def checkDebug(_argc: int, _argv: list[str]) -> tuple:
		for i in range(_argc):
			if _argv[i] == "-d" or _argv[i] == "--debug":
				return (True, i)
		return (False, -1)

	def checkFFmpeg(self):
		"""Checks whether FFmpeg is installed and on the system path"""
		try:
			_ffprobe = FFmpeg(executable = "ffprobe").option("h")
			_ffmpeg = FFmpeg().option("h")
			_ffprobe.execute()
			_ffmpeg.execute()
		except FileNotFoundError:
			self.errorConsole.log(f"[Fatal] checkFFmpeg() failed: could not find FFmpeg in path")
			self.errorConsole.log(f"- Make sure FFmpeg is installed and is in path before launching this script")
			raise SystemExit(127)

	def logMetadata(self):
		"""Prints the metadata of a media (MediaManager class) file"""
		_metadata = self.media.metadata
		self.console.log(f"[Info] Detected source info: ")
		self.console.log(f"[bold]- Video (source stream 1)", highlight = False)
		self.console.log(f"|    Video codec      : {_metadata['streams'][0]['codec_long_name']}", highlight = False)
		self.console.log(f"|    Video color      : {_metadata['streams'][0]['color_space']}", highlight = False)
		self.console.log(f"|    Video resolution : {_metadata['streams'][0]['width']}x{_metadata['streams'][0]['height']} pixels", highlight = False)
		self.console.log(f"|    Video framerate  : {self.framerate} fps", highlight = False)
		self.console.log(f"|    Video length     : {self.totalSecs} seconds", highlight = False)
		self.console.log(f"|    Total frames     : {self.totalFrame} frames", highlight = False)
		self.console.log(f"[bold]- Audio (source stream 2)", highlight = False)
		self.console.log(f"|    Audio codec      : {_metadata['streams'][1]['codec_long_name']}", highlight = False)
		self.console.log(f"|    Audio profile    : {_metadata['streams'][1]['profile']}", highlight = False)
		self.console.log(f"|    Audio samplerate : {_metadata['streams'][1]['sample_rate']}", highlight = False)
		self.console.log(f"|    Audio channels   : {_metadata['streams'][1]['channels']}", highlight = False)
		self.console.log(f"|    Audio layout     : {_metadata['streams'][1]['channel_layout']}", highlight = False)
		self.console.log(f"|    Audio bitrate    : {int(_metadata['streams'][1]['bit_rate']) // 1000}k", highlight = False)

	def process(self) -> None:
		"""Processes the input file by instantiating a MediaManager() object"""
		self.media = MediaManager(self.input)
		self.framerate: int  = self.media.getFramerate()
		self.totalSecs: int  = self.media.getTotalSecs()
		self.totalFrame: int = self.totalSecs * self.framerate

		self.logMetadata()
		if len(self.media.metadata['streams']) > 3:
			self.console.log()
			self.console.log(f"[red][Warning] Multiple video/audio streams detected")
			self.console.log(f"- Mpeg-compress has not been tested/designed with multiple video/audio streams in mind")
			self.console.log(f"- You are entering unknown territory if you proceed! ")
			self.console.log(f"- This could also be a false detection")

		self.media.askEncodeOptions()

	def convert(self) -> None:
		"""Starts the conversion of the media file"""

		self.ffmpegInstance = (FFmpeg()
			.option("y")
			.input(self.input)
			.output(
				self.output,
				self.media.options
			))

		self.lastFrame: int = 0

		with ProgressBar(
			TextColumn("[progress.description]{task.description}"),
			BarColumn(),
			TaskProgressColumn(text_format = "[progress.percentage]{task.percentage:>0.1f}% ({task.completed}/{task.total} frames)"),
			transient = True, 
			console = self.console
		) as _bar:

			@self.ffmpegInstance.on("progress")
			def updateProgress(_progress: Progress) -> None:
				_bar.update(_task, total = self.totalFrame)
				_bar.update(_task, advance = _progress.frame - self.lastFrame)
				self.lastFrame = _progress.frame

			@self.ffmpegInstance.on("start")
			def showArgs(_args: list[str]):
				self.console.log(f"[Info] Initiated FFmpeg task with the following command: {_args}")

			@self.ffmpegInstance.on("stderr")
			def ffmpegOutput(_Msg: str) -> None:
				if self.debug:
					self.console.log(f"[FFmpeg] {_Msg}")

			_task = _bar.add_task("[green]Transcoding file...", total = None)
			self.ffmpegInstance.execute()

	def run(self) -> None:
		"""The entrypoint of the program"""

		self.parseArgs()
		self.console.log(f"[Info] Parsed command-line arguments: '{self.input}' and '{self.output}'")

		try:
			self.process()
			self.convert()
		except FFmpegError as _error:
			_ffmpegArgs = ""
			for _arg in _error.arguments:
				_ffmpegArgs = _arg + " "

			self.errorConsole.log(f"[Fatal] An FFmpeg exception has occured!")
			self.errorConsole.log(f"[bold][red]- Error message from FFmpeg: [/bold][/red][white][not bold]{_error.message.lower()}", highlight = False)
			self.errorConsole.log(f"[bold][red]- Arguments to execute FFmpeg: [/bold][/red][white][not bold]{_ffmpegArgs.lower()}", highlight = False)
			self.errorConsole.log(f"[Info] Exiting mpeg-convert...")
			raise SystemExit(1)

		self.console.log(f"[green][Info] Succesfully executed mpeg-convert")
		return


if __name__ == "__main__":
	try:
		traceback.install(show_locals = True)
		instance = Program()
		instance.run()
		raise SystemExit(0)
	except KeyboardInterrupt:
		Console().print()
		Console().log("[Warning] Program received KeyboardInterrupt...")
		Console().log("[Warning] Force quitting with os._exit()...")
		os._exit(0)   # Force terminate all threads
