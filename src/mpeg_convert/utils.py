import os
import sys
import platform
import subprocess

from rich.console import Console


HELP_TEXT = ("\
Usage: mpeg-convert \\[options] <file.in> <file.out>                 \n\
                                                                        \n\
Required args:                                                          \n\
    file.in        The path to the file to convert from                 \n\
    file.out       The path to the file to output to                    \n\
                                                                        \n\
Optional args:                                                          \n\
    --version       Prints the version information to the console       \n\
    --customize     Opens customization.py in your default text editor  \n\
    -h  --help      Prints this help text and exits                     \n\
    -v  --verbose   Outputs all ffmpeg log to the console               \n\
    -d  --default   Use all default options (customizable from script)  \n\
                                                                        \n\
Custom encoders can be listed by 'ffmpeg -codecs'. Additionally, FFmpeg \n\
will automatically detect the file extensions/containers to convert     \n\
to/from; you do not need to specify anything.                           \n\
                                                                        \n\
Head to https://github.com/SomedudeX/mpeg-convert/blob/main/README.md   \n\
for more documentation on mpeg-convert.                                   \
")


VERSION = "v0.0.1"

    
def print_help():
    """Prints the help usage to the console"""
    Console().print(HELP_TEXT, highlight = False)
    
    
def print_version():
    """Prints the version information to the console"""
    _prgram_version = VERSION
    _python_version  = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    _system_version = f"{sys.platform.capitalize()} ({platform.architecture()[0]} {platform.machine()})"
    
    Console().print(f"Program  : {_prgram_version}", highlight = False)
    Console().print(f"Python   : {_python_version}", highlight = False)
    Console().print(f"Platform : {_system_version}", highlight = False)


def readable_size(_path: str, _decimal_point = 2) -> str:
    """Calculates the size of a particular file on disk and returns the
    size in a human-readable fashion
    """
    size: float = os.path.getsize(_path)
    
    for i in ["bytes", "kb", "mb", "gb", "tb", "pb"]:
        if size < 1024.0:
            return f"{size:.{_decimal_point}f} {i}"
        size /= 1024.0
        
    return f"{size:.{_decimal_point}f} pb"
    
    
def handle_customize() -> None:
    file_path = os.path.realpath(__file__)
    file_dir = os.path.dirname(file_path)
    Console().log("[Info] Opening customization options", highlight = False)
    
    if platform.system() == "Darwin":
        subprocess.call(["open", f"{file_dir}/customization.py"])
    elif platform.system() == "Windows":
        os.startfile(f"{file_dir}/customization.py")
    else: 
        subprocess.call(["xdg-open", f"{file_dir}/customization.py"])
    Console().log(
        "[Info] Succesfully opened customization options in default text editor", 
        highlight = False
    )
    
    return
    

class ModuleCheck():
    
    @staticmethod
    def check_required() -> None:
        try:
            import rich
            import ffmpeg
        except ModuleNotFoundError as e:
            _error = str(e)
            print(f" \033[91m[Fatal] Module missing: {_error.lower()}")
            print(f" - Make sure you install all required modules by using 'pip'")
            print(f" - Make sure you are using the correct version of python\033[0m")
            print(f" - Mpeg-convert terminating with exit code -1")
            raise SystemExit(-1)
        return
        
    @staticmethod
    def check_customize() -> None:
        try:
            from . import customization
        except Exception as e:
            print(f" \033[91m[Fatal] Customization script is invalid or incorrectly formatted")
            print(f" - Error message: {str(e)}")
            print(f" - Mpeg-convert terminating with exit code -1")
            raise SystemExit(-1)
        return
            

class FatalError(Exception):
    """Represents a fatal error encountered during the execution of the program"""
    
    def __init__(
        self,
        _error_code: int = 1,
        _error_msg: str = "An unknown fatal error occured",
        *_notes: str
    ) -> None:
        """Initializes a FatalError object"""
        self.msg  = f"[Fatal] {_error_msg}"
        self.code = f"{_error_code}"
        self.note = f""
        for note in _notes:
            self.note += f"\n{note}"
        
        self.note = self.note[1:]
        return
