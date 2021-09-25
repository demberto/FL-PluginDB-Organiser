# FL Studio Plugin Database Organizer

Reads plugin database files (.nfo) created by FL Studio and reorganizes them into folders based on plugin vendor names.
Only for Windows

## Requirements
* Python 3.6+
* Windows

## Usage
1. Clone this repo or just download [`fl_plugin_db_organiser.py`](fl_plugin_db_organiser.py).
2. Open `cmd`, browse to the folder you downloaded/cloned.
3. Enter `python fl_plugin_db_organiser.py <location_to_output_new_folders>`.
4. Copy **Effects** and **Generators** folders to `%USERPROFILE%/Documents/Image-Line/FL Studio/Presets/Plugin database/` to see them in FL.

A log file will be generated as well in the folder `fl_plugin_db_organiser.py` is in.



## NOTE
This DOES NOT categorize your VST2/3 plugin install folders by vendor
name, so its useful only after FL scans and creates the database. This script
will only work when you haven't modified the structure of `%USERPROFILE%/Documents/Image-Line/FL Studio/Presets/Plugin database/Installed` folders as created by FL.
While running you might see some warnings, no need to
worry about them if they are from iZotope plugins (name begins with 'iZ').

If you want to categorize native plugins as well, just copy the 'Fruity'
folders from **Effects** and **Generators** folders at `%USERPROFILE%/Documents/Image-Line/FL Studio/Presets/Plugin database/` to newly created ones and rename them to *Image-Line* or whatever you like.

If you see vendor folders named `SynthEdit www.synthedit.com`, its because
plugin developer is using trial version of SynthEdit, actual plugin vendor
is stored neither in the .nfo nor the VST itself.

## License
MIT License