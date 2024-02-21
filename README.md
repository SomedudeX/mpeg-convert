## MPEG-Convert

A highly customizable<sup>[1](#Customizing)</sup> terminal-based [Python](https://www.python.org/downloads/) wrapper for [FFmpeg](https://ffmpeg.org/download.html) that provides a humanized approach to conversions between different multimedia formats. 

FFmpeg is a powerful multimedia tool, but its many options<sup>[2](https://ffmpeg.org/ffmpeg.html)</sup> can be especially overwhelming for new users. This wrapper aims to simplify the process of working with the FFmpeg engine to convert between different video/audio formats for the folks who doesn't want to memorize twenty options to use FFmpeg. This program is not, however, a complete replacement for FFmpeg in any way. For that purpose, you should look look into other software such as [Handbrake](https://handbrake.fr/) or [DaVinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve). 

This project is now hosted on [PyPi](https://pypi.org/project/mpeg-convert), however legacy releases can still be found on the right. 

## Features

* **Simplified commands**: MPEG-Convert provides a straightforward interface for commonly used FFmpeg functionalities, making it easy for both beginners and experienced users to perform tasks such as codec conversion, audio extraction, video compression, and much more.

* **Configurability**: While MPEG-Convert is designed for simplicity, it also provides room for customization<sup>[1](#Customizing)</sup>. You can tweak advanced settings by specifying additional FFmpeg options in the script or during script execution, ensuring flexibility for more sophisticated multimedia processing needs.

![demo](https://github.com/SomedudeX/MPEG-Convert/assets/101906945/d69c68b0-4122-4ebc-a6fb-3de50448dcd0)

## Installation 

Make sure you have Python 3 and FFmpeg installed. 

```bash
pip install --upgrade mpeg-convert
mpeg-convert --help
```

## Customizing

#### Interactive

You can customize the interactive mode of the script by changing the questions variable `VIDEO_OPTIONS` and `AUDIO_OPTIONS` in mpeg-convert to your liking. This can be achieved using the `--customize` option, which will open the correct file for you in your default text editor.

The two variables represents the list of questions asked during video options and audio options sections of the script respectively. The properties of each question is represented as a dictionary in python, and will be shown to the user in order. The dictionaries' format is shown below:

```py
[
    {
        "type": <str>,
        "title": <str>,
        "option": <str>,
        "default": <int>,
        "choices": <list[tuple]>
    }
]
```

 * **`type`**: The type of the question

   * Valid values:
     + **`choice`**: Multiple choice
     + **`input`**: Input field

 * **`title`**: The text shown to the console when displaying the question during the execution of the program

 * **`option`**: The corresponding option in FFmpeg. This option will be inserted to the list of arguments passed to FFmpeg

 * **`default`**: The default option that is used when the input field is empty. Has no effect if question type is `input`.

 * **`choices`**: A list of choices that will be shown to the console during the execution of the program. The choices will be in tuples where the first index will be what is displayed, and the second index is what is actually entered as a value for the particular FFmpeg option. Has no effect if question type is `input`.

An example of a custom question is below: 

```py
[
    {
        "type": "choice",
        "title": "Select an encoding preset",
        "option": "-preset",
        "default": 3,
        "choices": [
            ("Faster/lower quality", "veryfast"),
            ("Normal/medium quality", "medium"),
            ("Slower/best quality", "veryslow")
        ]
    }
]
```

<br></br>

#### Presets

Presets are different predetermined flags and options of FFmpeg options that mpeg-convert uses when you specify the name of the preset. Presets can be activated by specifying the name of the preset as a positional flag. You can customize them by modifying the `PRESETS` variable also located in `customization.py`. 

The preset's format is shown below: 
```py
{
    "name": {
        "option": <str>,
        "option": <str>,
        "option": <str>,
        ...
    }
}
```

 * **`name`**: The name that is used to activate the preset

 * **`option`**: A command-line option to be inserted to the list of arguments passed to FFmpeg. The option should be stripped of the dash (-) symbol at the front. If the FFmpeg option does not take any value, put `None` after the colon. There can be more than one option in each preset. 
 
An example of a custom preset is below:

```py
{
    "flac-audio": {
        "vn": None,
        "ar": "96000",
        "codec:a": "flac",
        "sample_fmt": "s24",
    }
}
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

## Resources

 - [Demo](https://github.com/SomedudeX/mpeg-convert/raw/main/demo.mp4)
 - [License](https://raw.githubusercontent.com/SomedudeX/mpeg-convert/main/LICENSE)
 - [Project](https://pypi.org/project/mpeg-convert/)

Contributions are welcome! If you encounter any problems or find any bugs, please feel free to open an issue. In the meantime, happy converting! 

--
