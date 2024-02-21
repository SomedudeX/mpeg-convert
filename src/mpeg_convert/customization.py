# -*- coding: utf-8 -*-

# -*- Customization -*-
#
# The options specified below are presented to you when converting a file. You
# can customize these options to your liking. For more information/documentation
# on how to customize these questions and parameters, head to the following link:
#
# https://github.com/SomedudeX/mpeg-convert/tree/main?tab=readme-ov-file#customizing


# Use 'HEVC_ENCODER' and 'H264_ENCODER' for
# H.264/5 encoding, especially if you're on macOS

from src.mpeg_convert.utils import HEVC_ENCODER, H264_ENCODER


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
# you use the '-d' or '--default' flag. The keys represent an ffmpeg option (stripped  
# of the '-' in front), and the value represent the values (duh). 
#
# e.g. { "preset": "veryslow" } is the equivalent of '-preset veryslow'

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
