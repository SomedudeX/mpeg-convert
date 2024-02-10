# -*- coding: utf-8 -*-


# -*-  Style guide  -*-
#
# This project uses the following styles for token names
#
#     PascalCase       Class name
#     snake_case       Variable or function/method name
#     _underscore      Variable/function should be used only intenally in
#                      the scope it's declared in (and should not be
#                      modified by the end user)
#
# Because python does not have a reliable way of signalling the end
# of a particular scope, method, or class, any class/method in this 
# file will always terminate in `return` regardless of the return
# type. 
#
# In addition, python's native type hinting is used whenever possible
# in order to catch issues and minimize problems with static analyzers
#
# This project uses 4 spaces for indentation. 


# -*- Customization -*-
#
# The options specified below are presented to you when converting a file. You
# can customize these options to your liking. For more information/documentation
# on how to customize these questions and parameters, head to the following link:
#
# https://github.com/SomedudeX/MPEG-Convert/tree/main?tab=readme-ov-file#customizing


from sys import platform

HEVC_ENCODER = "libx265"
H264_ENCODER = "libx264"

# On macOS, use apple's 'videotoolbox'
# for faster encoding speed
if platform == "darwin":
    HEVC_ENCODER = "hevc_videotoolbox"
    H264_ENCODER = "h264_videotoolbox"


VIDEO_OPTIONS = [

    {
        "type": "choice",
        "title": "Video resolution...",
        "option": "-s",
        "default": 2,
        "choices": [
            ("1280x720", "1280x720"),
            ("1920x1080", "1920x1080"),
            ("2560x1440", "2560x1440"),
            ("3840x2160", "3840x2160"),
        ]
    },
    
    {
        "type": "choice",
        "title": "Video framerate...",
        "option": "-r",
        "default": 1,
        "choices": [
            ("24 fps", "24"),
            ("30 fps", "30"),
            ("48 fps", "48"),
            ("60 fps", "60"),
        ]
    },
    
    {
        "type": "choice",
        "title": "Video codec...",
        "option": "-c:v",
        "default": 2,
        "choices": [
            ("H.264", H264_ENCODER),
            ("H.265", HEVC_ENCODER),
            ("AV1", "libsvtav1"),
            ("VP9", "libvpx-vp9"),
        ]
    },
    
    {
        "type": "choice",
        "title": "Video quality...",
        "option": "-crf",
        "default": 2,
        "choices": [
            ("CRF 18", "18"),
            ("CRF 21", "21"),
            ("CRF 24", "24"),
            ("CRF 32", "32"),
        ]
    }
]

AUDIO_OPTIONS = [

    {
        "type": "choice",
        "title": "Audio codec...",
        "option": "-c:a",
        "default": 2,
        "choices": [
            ("AAC", "aac"),
            ("MP3", "libmp3lame"),
            ("ALAC", "alac"),
            ("FLAC", "flac"),
        ]
    },
    
    {
        "type": "choice",
        "title": "Audio bitrate...",
        "option": "-b:a",
        "default": 2,
        "choices": [
            ("96k", "96k"),
            ("128k", "128k"),
            ("192k", "192k"),
            ("320k", "320k")
        ]
    },
    
    {
        "type": "choice",
        "title": "Audio samplerate...",
        "option": "-ar",
        "default": 2,
        "choices": [
            ("16000hz", "16000"),
            ("44100hz", "44100"),
            ("48000hz", "48000"),
            ("96000hz", "96000")
        ]
    }
]

# The options specified below are the default options that the program will use when 
# you use the '-d' or '--default' flag. 

DEFAULT_OPTIONS = {
    "r": "24",
    "s": "1920x1080",
    "c:v": H264_ENCODER,
    "c:a": "libmp3lame", 
    "b:a": "192k", 
    "ar": "44100", 
    "crf": "21", 
    "ac": "2"
}
