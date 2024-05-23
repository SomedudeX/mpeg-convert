A customizable<sup>[1](#Configuring)</sup> tool that provides some quality-of-life additions for [FFmpeg](https://ffmpeg.org). This tool adds features such as pretty printing, progress bars, and command presets.

## Installation 

Ensure [Python](https://www.python.org/downloads/) and [FFmpeg](https://ffmpeg.org/download.html) is installed. Then, use the [Python Packaging Index](https://pypi.org/) (PyPI) to install `mpeg-convert` and its dependencies. You may need to use `pip3` instead of `pip` in certain environments: 

```bash
$ pip install --upgrade mpeg-convert
$ mpeg-convert --help
```

This tool does not aim to replace FFmpeg or any other conversion software such as [Handbrake](https://handbrake.fr/). Rather, it tries to improve the user experience and productivity when using FFmpeg. See [usages](#Usage) and [configuring](#Configuring) for more details. 

## Usage

The most basic way to use `mpeg-convert` is to specify an input file path and an output file path. `mpeg-convert` will then call FFmpeg to initiate the conversion, and display a bar indicating the progress of the conversion. No extra FFmpeg options will be added when transcoding the file. This is demonstrated with the command and screenshot below: 

```bash
$ mpeg-convert sample.mp4 output.mov
```

<img width="840" alt="Screenshot 2024-05-22 at 17 47 27" src="https://github.com/SomedudeX/mpeg-convert/assets/101906945/4cde6fe7-e079-47f0-b82b-f07528fdcffd">

For conversions where you may need or want to tweak extra options (e.g. frame rate, constrast, or bitrate changes), you can add a named or unnamed preset by following the [configuration guide](#Configuring). After you have saved your custom preset to the config file, you can use it by using the `--preset` flag for named presets, or convert between matching file containers/extensions for unnamed presets. This will use the extra custom FFmpeg options you specified in the preset when transcoding. This is demonstrated below:

```bash
$ mpeg-convert sample.mp4 output.mov --preset="custom-1080p"
```

<img width="841" alt="Screenshot 2024-05-22 at 18 00 35" src="https://github.com/SomedudeX/mpeg-convert/assets/101906945/9b9c4b54-9465-4dfa-94fc-6ad355f13009">

As of writing, presets are the only method to use FFmpeg options while converting with `mpeg-convert`. Additionally, multiple inputs and other advanced FFmpeg features are not supported by `mpeg-convert`. Such feature is unlikely to be added to `mpeg-convert`, since it is written as a complement, not replacement, to FFmpeg; consider directly using FFmpeg or other UI based programs such as Handbrake for such tasks. 

## Configuring

**Presets** allows you to save FFmpeg commands for repeated use, eliminating the need to enter long and complex flag/options each time you need to convert or edit media files. You can add presets to `mpeg-convert` by editing the YAML configuration file. To open the config, use the `--config` flag as demonstrated below:

```bash
$ mpeg-convert --config
```

There are two types of presets you can specify in the config file: named presets and unnamed presets.

 * **Named presets** are invoked when you explicitly use the `--preset` flag. You can add a named preset under the `named` key. Each named preset must have a unique name and a string of ffmpeg options. To activate a named preset, specify its name with the `--preset` flag, and `mpeg-convert` will use the options when converting. An example of a named preset is below:

```yml
named:
- name: "custom-1080p"
  options: "-vf scale=1920x1080 -r 24"
```

 * **Unnamed presets** are applied automatically to conversions of specific file types and extensions. They are useful when you want conversions between one container type and another container type to always use certain FFmpeg options. Each unnamed preset must have an array of file extensions in `from-type` and `to-type`, and a string of FFmpeg options; and voilà, whenever you convert between any of the file extensions in `from-type` to any of the extensions in `to-type`, `mpeg-convert` will automatically use the FFmpeg options specified in the unnamed preset. An example of an unnamed preset is below:

```yml
unnamed:
- from-type: ["mp4", "mov"]
  to-type: ["gif"]
  command: "-vf scale=1280x720 -r 8"
```

If you have an unnamed preset specified for a file type you are converting to/from, but you would like to temporarily disable it, you can use the `--plain` flag. This will remove any FFmpeg options for the current conversion.

When searching for matching presets, `mpeg-convert` will check using the following order:
 * Check if `--plain` flag is specified. If not...
 * Check if `--preset` flag is specified. If not...
 * Check if there is a matching unnamed preset. If not...
 * Initiate the conversion without any FFmpeg commands

## Troubleshooting

* Do you have python installed?
* Do you have ffmpeg installed?
* Common pitfalls:
  + Does the output file have an extension?
  + Does the extension match the codec?
    - `HEVC` with `.mp4`
    - `ALAC` with `.m4a`
  + Is the encoder installed on your system?

## Notes

This project has undergone substantial changes in `v0.2.0`. Click [here](https://github.com/SomedudeX/mpeg-convert/blob/15f4026633c5da667e6283cdeb78d82b29cd1b3d/README.md) if you are looking for documentation before `v0.2.0`

--
