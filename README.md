# FL Studio Plugin Database Organiser
Reads plugin database files (.nfo) created by FL Studio and reorganises them into folders based on plugin vendor names.

## Requirements
Python 3.4+ on Windows

## Installation
Via pip (**RECOMMENDED**)
```
python -m pip install --upgrade fl_plugin_db_organiser
```

*or* manually,

* Clone this repo
* Optionally, install dependency `ansicolors` if you want colored output

## Usage
```
fl-plugindb-organizer [-h] [--log LOG] [--no-color] output

positional arguments:
  output             Path to output database folders

optional arguments:
  -h, --help         show this help message and exit
  --log LOG, -l LOG  Location to output log file to, defaults to ./fl-plugindb-organizer.log
  --no-color         Disable colored output, necessary if you haven't installed ansicolors
```

Example: `fl-plugindb-organiser .` will output
* A log in the current working directory named `fl-plugindb-organiser.log`, *and* 
* Create 2 folders **Effects** and **Generators**, which need to copied over to `%USERPROFILE%/Documents/Image-Line/FL Studio/Presets/Plugin database` for FL Studio to detect it.

## NOTES
This script will only work when you haven't modified the structure of `%USERPROFILE%/Documents/Image-Line/FL Studio/Presets/Plugin database/Installed` folders as created by FL.
While running you might see some warnings, this can be for two reasons:
* The vendor name contains prohibited characters, Windows doesn't allow folder/file names to contain them `:, /, \\, ", *, |, ?, <, >`
* Some `.nfo` files don't have a corresponding `.fst`, if this is happening for certain iZotope plugins (i.e names starting with 'iZ'), then its normal, iZotope DLLs pollute the VST install folders with DLLs not actually plugins

If you want to categorize native plugins as well, just copy the **Fruity** folders from **Effects** and **Generators** folders at `%USERPROFILE%/Documents/Image-Line/FL Studio/Presets/Plugin database/` to newly created ones and rename them to *Image-Line* or whatever you like.

If you see vendor folders named `SynthEdit www.synthedit.com`, its because plugin developer is using trial version of SynthEdit, actual plugin vendor is stored neither in the .nfo nor the VST itself.

## TODO
* Support for Mac: If you are a Mac user who wants to use this, please open an issue with details on where the plugin database is located.
* Maybe support to copy the new plugin database automatically to where it is stored by FL and backing up existing one.
* Use other method for organizing, but so far I think organizing by vendor names is the best way.
* Organize native plugins as well under an **Image-Line** folder, is it really required?
* A [test script](tests/test_script.py)

## License
MIT License