## MPEG-Convert
A python tool based on ffmpeg that makes converting between different formats/codecs a whole lot easier for the end-user

## Installation
* Clone this repository
  ```bash
  git clone https://github.com/SomedudeX/MPEG-Convert
  ```
* Install dependencies
  ```bash
  cd MPEG-convert
  pip3 install -r requirements.txt
  ```
* Launch the script
  ```
  ./mpeg-convert.py
  ```
> [!NOTE]
> You do not need to use `python3 mpeg-convert.py` because of the shebang at the top

If you would like to launch this script from anywhere, you can add it to the path (duh)

## Troubleshooting

* Do you have python installed?
* Do you have ffmpeg installed?

## Usage
```
Usage: mpeg-convert <filepath.in> <filepath.out>

This tool is a simple wrapper for the ffmpeg engine to make the
conversion between different video/audio formats a little easier for
the everyday user. This program is not, however, a complete
replacement for ffmpeg in any way. For that purpose, you should look
look into other software such as Handbrake or DaVinci Resolve.

Additionally, this tool has been hacked together in a couple of
days, meaning that some of the finer details has not been fleshed
out yet -- expect some rough corners during use. This tool also has
not been tested or designed for multiple video/audio streams.

Notes:
    The default (and only) CRF value is 21. You can change it in
    the script itself if you'd like.

    FFmpeg will automatically detect the file extensions/containers
    to convert to/from; you do not need to specify anything.
```
--
```
Last updated Jan 2023
Not in active development
```
