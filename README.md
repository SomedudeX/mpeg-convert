## MPEG-Convert

A highly customizable<sup>[1](#Customizing)</sup> terminal-based [Python](https://www.python.org/downloads/) wrapper for [FFmpeg](https://ffmpeg.org/download.html) that provides a humanized approach to conversions between different multimedia formats. 

FFmpeg is a powerful multimedia tool, but its many options<sup>[2](https://ffmpeg.org/ffmpeg.html)</sup> can be especially overwhelming for new users. This wrapper aims to simplify the process of working with the FFmpeg engine to convert between different video/audio formats for the folks who doesn't want to memorize twenty options to use FFmpeg. This program is not, however, a complete replacement for FFmpeg in any way. For that purpose, you should look look into other software such as [Handbrake](https://handbrake.fr/) or [DaVinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve). 

Additionally, this tool has been hacked together in a couple of weeks, meaning that some of the finer details has not been fleshed out or extensively tested — expect some rough corners during use. This tool also has not been tested or designed for multiple video or audio streams. 

## Features

* **Simplified commands**: MPEG-Convert provides a straightforward interface for commonly used FFmpeg functionalities, making it easy for both beginners and experienced users to perform tasks such as codec conversion, audio extraction, video compression, and much more.

* **Configurability**: While MPEG-Convert is designed for simplicity, it also provides room for customization<sup>[1](#Customizing)</sup>. You can tweak advanced settings by specifying additional FFmpeg options in the script or during script execution, ensuring flexibility for more sophisticated multimedia processing needs.

![demo](https://github.com/SomedudeX/MPEG-Convert/assets/101906945/d69c68b0-4122-4ebc-a6fb-3de50448dcd0)

## Installation 

Make sure you have Python 3 and FFmpeg installed. 

#### Automatic

```bash
eval "$(curl -s https://raw.githubusercontent.com/SomedudeX/MPEG-Convert/main/install.sh)"
```

> [!IMPORTANT]
> For macOS users, make sure to go into the script and do a global find-and-replace from `libx264` to `h264_videotoolbox` and from `libx265` to `hevc_videotoolbox`.
>
> This is necessary because the regular `libx264` and `libx265` encoder is horribly slow on macOS. By using Apple's own encoders, you can get much faster encoding results.

#### Manual

* Clone this repository
  
  ```bash
  git clone https://github.com/SomedudeX/MPEG-Convert.git
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
  
You may need to add execution privileges to the script by `sudo chmod +x` in order to execute it. Additionally, if you would like to run this script from anywhere in the terminal, you can add the script's path to your environment's `$PATH` variable. 

> [!WARNING]
> The manual installation instructions are designed for POSIX-compliant shells (Linux/macOS) and are not tested for Windows. 

## Customizing

You can further customize the script by changing the questions variable `VIDEO_OPTIONS`<sup>[3](https://github.com/SomedudeX/MPEG-Convert/blob/main/App/mpeg-convert.py#L35)</sup> and `AUDIO_OPTIONS`<sup>[4](https://github.com/SomedudeX/MPEG-Convert/blob/main/App/mpeg-convert.py#L90)</sup> in mpeg-convert.py to your liking. 

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
   + **`choice`**: Multiple choice
   + **`input`**: Input field
  
> [!NOTE]
> If a question type is set to `choice`, MPEG-Convert will automatically append `custom value` and `remove option` as the last two options. 

**`title`**: The text shown to the console when displaying the question during the execution of the program

**`option`**: The corresponding option in FFmpeg. This option will be inserted to the list of arguments passed to FFmpeg

**`default`**: The default option that is used when the input field is empty. Has no effect if question type is `input`.

**`choices`**: A list of choices that will be shown to the console during the execution of the program. The choices will be in tuples where the first index will be what is displayed, and the second index is what is actually entered as a value for the particular FFmpeg option. Has no effect if question type is `input`.

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
            ("Slower/best quality", "veryslow")
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

## Resources

 - [Demo](https://github.com/SomedudeX/MPEG-Convert/raw/main/Demo/demo.mov)
 - [License](https://raw.githubusercontent.com/SomedudeX/MPEG-Convert/main/LICENSE)
 - [Releases](https://github.com/SomedudeX/MPEG-Convert/releases)

Contributions are welcome! If you encounter issues or have suggestions for improvements, please feel free to open an issue or submit a pull request. In the meantime, happy converting! 

--
