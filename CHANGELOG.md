# 1.1.0

Added Mac support #1 @zacanger

# 1.0.14
## Bug fixes
Fix logging level incorrectly set to `logging.CRITICAL`. Logging will now happen correctly.

# 1.0.13
## Bug fixes
Fix import errors in script

# 1.0.0 (2021-09-26)
FL Plugin DB Organiser is now on [pip](https://pypi.org/project/fl-plugin-db-organiser)

## Additions
* Colored output, can be disabled by passing `--no-color`.
* Packaged as a python script, once installed via pip can be invoked from cmd by `fl-plugindb-organiser` directly.
* Support for Python 3.4+

## Changes
* Updated the [README](README.md) to specify the new install method and made it more clear.

## Bug fixes
* Fixed folder creation errors when vendor name contains prohibited characters.

# Initial release (2021-09-25)