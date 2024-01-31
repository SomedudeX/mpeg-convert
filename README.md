## MPEG-Convert
A terminal-based [Python](https://www.python.org/downloads/) wrapper for [FFmpeg](https://ffmpeg.org/download.html) that makes converting between different formats/codecs a whole lot easier for the end-user

This wrapper makes using the FFmpeg engine to convert between different video/audio formats a lot easier for the folks who doesn't want to memorize twenty options to use FFmpeg. This program is not, however, a complete replacement for FFmpeg in any way. For that purpose, you should look look into other software such as Handbrake or DaVinci Resolve. 

Additionally, this tool has been hacked together in a couple of weeks, meaning that some of the finer details has not been fleshed out or extensively tested — expect some rough corners during use. This tool also has not been tested or designed for multiple video or audio streams. 

![demo](https://github.com/SomedudeX/MPEG-Convert/assets/101906945/d69c68b0-4122-4ebc-a6fb-3de50448dcd0)

## Installation 

* Clone this repository
  
  ```bash
  git clone https://github.com/SomedudeX/MPEG-Convert/tree/main
  cd MPEG-Convert
  ```

* Install script dependencies

  ```bash
  python -m pip install -r requirements.txt
  ```

* Launch the script

  ```bash
  ./App/mpeg-convert.py --help
  ```
  
> [!NOTE]
> You may need to `sudo chmod +x` the script in order to run it

## Usage
```
A media file converter using the ffmpeg engine. 

Usage: mpeg-convert [options] <filepath.in> <filepath.out>

Options:
	-h   --help        Shows the help page
	-v   --verbose     Enable debug mode to see FFmpeg logs
	-d   --default	   Use all default settings

Custom encoders can be listed by `ffmpeg -codecs`. Additionally,
FFmpeg will automatically detect the file extensions/containers
to convert to/from; you do not need to specify anything.
```

## Customizing

You can further customize the script by changing the questions variable `VIDEO_OPTIONS` and `AUDIO_OPTIONS` in mpeg-convert.py to your liking. 

The two variables represents the list of questions asked during video options and audio options sections of the script respectively. The properties of each question is represented as a dictionary in python, and will be shown to the user in order. The dictionaries' format is shown below:

```py
[
...
    {
        "type": <str>,
        "title": <str>,
        "option": <str>,
        "default": <int>,
        "choices": <list[tuple]>
    }
...
]
```

**`type`**: The type of the question

 * Valid values:
   - **`choice`**: Multiple choice
   - **`input`**: Input field

**`title`**: The text shown to the console during the execution of the program

**`option`**: The corresponding option to insert to the list of arguments passed to FFmpeg

**`default`**: The default option that is used when the input field is empty (no effect if type is `input`)

**`choices`**: A list of choices that will be shown to the console during the execution of the program. The choices will be in tuples where the first index will be what is displayed, and the second index is what is actually entered as a value for the particular FFmpeg option

An example of a custom question is below: 

```py
[
...
    {
        "type": "choice",
        "title": "Select an encoding preset",
        "option": "-preset",
        "default": 3,
        "choices": [
            ("Faster/lower quality", "veryfast"),
            ("Normal/medium quality", "medium"),
            ("Slower/best quality", "veryslow)
        ]
    }
...
]
```

## Troubleshooting

* Do you have python installed?
* Do you have ffmpeg installed?
* Common pitfalls:
  + Does the output file have an extension?
  + Does the extension match the codec?
    - `HEVC` with `.mp4`  
    - `ALAC` with `.m4a`
  + Is the encoder installed on your system?

--
