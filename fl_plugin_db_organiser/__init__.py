import argparse
import configparser
import importlib
import logging
import os
import pathlib
import shutil
import sys
from typing import Dict, List

FL_PLUGINDB_ORGANISER = "fl-plugindb-organizer"

PROHIBITED_FOLDER_NAME_CHARS = ':/\\"*|?<>'
COLORS = None   # Stores ansicolors module if required


class PluginDatabaseNotFoundError(Exception):
    """Raised when plugin database folder is not found"""

    def __init__(self, fl_plugin_db_dir: pathlib.Path) -> None:
        self._fl_plugin_db_dir = str(fl_plugin_db_dir)
        super().__init__()

    def __repr__(self) -> str:
        return "Could not find plugin database at " + self._fl_plugin_db_dir


# region Coloring
def _green(string: str):
    if COLORS:
        return COLORS.green(string)
    return string


def _blue(string: str):
    if COLORS:
        return COLORS.blue(string)
    return string


def _yellow(string: str):
    if COLORS:
        return COLORS.yellow(string)
    return string


def _red(string: str):
    if COLORS:
        return COLORS.red(string)
    return string
# endregion


def fl_plugin_db_organiser(output_dir: pathlib.Path, log: logging.Logger, no_color: bool):
    """Entry-point to the script.

    Args:
        output_dir (pathlib.Path): Absolute path to save the plugin database folders.
        log (logging.Logger): Logger to log to a file.
        no_color (bool): Doesn't output colored text to terminal if `True`.
    """

    # region Check for dependency
    if not no_color:
        try:
            global COLORS
            COLORS = importlib.import_module('colors')
        except ImportError:
            log.critical("Requested colored output when required "
                         "dependency 'ansicolors' is not present")
            print(
                _red("The 'ansicolors' module could not be found,"
                     "you can install it via 'pip install ansicolors'"
                     "or run this script with '--no-color' option to"
                     "disable colored output.")
            )
            sys.exit(-1)
    # endregion

    # region Init
    os.chdir(str(output_dir))
    generators = output_dir / "Generators"
    effects = output_dir / "Effects"

    # Create 'Generators' and 'Effects' folders
    log.info("Creating 'Effects' folder")
    print("Creating %s folder" % _green('Effects'))
    if not effects.is_dir():
        effects.mkdir()

    log.info("Creating 'Generators' folder")
    print("Creating %s folder" % _green('Generators'))
    if not generators.is_dir():
        generators.mkdir()
    # endregion

    # region Gather .nfo/.fst locations
    log.info("Finding existing database locations")
    print(_yellow("Finding existing database locations..."))

    fl_plugin_db_dir = pathlib.Path(
        os.path.expanduser(
            "~/Documents/Image-Line/FL Studio/Presets/Plugin database/Installed/"
        )
    )

    if not fl_plugin_db_dir.is_dir():
        raise PluginDatabaseNotFoundError(fl_plugin_db_dir)

    vst2_effect_db_dir = fl_plugin_db_dir / "Effects/VST"
    vst3_effect_db_dir = fl_plugin_db_dir / "Effects/VST3"
    vst2_generator_db_dir = fl_plugin_db_dir / "Generators/VST"
    vst3_generator_db_dir = fl_plugin_db_dir / "Generators/VST3"
    # endregion

    config_parser = configparser.ConfigParser()

    # region Discover .nfos, warn user of any missing folders.
    for folder in (vst2_effect_db_dir, vst2_generator_db_dir,
                   vst3_effect_db_dir, vst3_generator_db_dir):

        fsts = {}   # type: Dict[str, List[pathlib.Path]]
        nfos = []   # type: List[pathlib.Path]

        message = "Scanning %s"
        log.info(message % str(folder))
        print(message % _blue(str(folder)))

        if folder.is_dir():
            nfos.extend(tuple(folder.glob('*.nfo')))
        else:
            log.warn("%s doesn't exist or isn't a folder" % str(folder))

        # region Read vendor names from each .nfo and populate fsts.
        log.info("Finding vendor names")
        print("Finding vendor names...")
        for nfo in nfos:
            stream = open(str(nfo)).read()
            config_string = "[dummy_section]\n" + stream
            config_parser.read_string(config_string)

            dummy_section = config_parser['dummy_section']
            vendor = dummy_section.get('ps_file_vendorname_0')

            if vendor:
                fst = nfo.with_suffix('.fst')
                if fst.is_file():
                    if vendor not in fsts:
                        fsts[vendor] = []
                    fsts[vendor].append(fst)
                else:
                    message = "No corresponding .fst found for %s"
                    log.warn(message % str(nfo))
                    print(message % _yellow(str(nfo)))
            else:
                message = "Couldn't find vendor name from %s"
                log.warn(message % str(nfo))
                print(message % _yellow(str(nfo)))

        vendors = tuple(fsts.keys())
        message = "Found %s vendors: %s"
        log.info(message % (len(vendors), vendors))
        print(message % (_green(len(vendors)), vendors))
        # endregion

        # region Create folders with vendor names and copy .fst to them
        if folder in (vst2_generator_db_dir, vst3_generator_db_dir):
            os.chdir(str(generators))
        else:
            os.chdir(str(effects))

        message = "Creating new plugin database at %s"
        cwd = os.getcwd()
        log.info(message % cwd)
        print(message % _blue(cwd))
        for vendor in fsts:
            if not os.path.isdir(vendor):
                log.debug("Creating vendor folder %s" % vendor)
                vendor_safestr = vendor.strip(PROHIBITED_FOLDER_NAME_CHARS)
                if vendor != vendor_safestr:
                    message = "Vendor name '%s' contains prohibited characters" % vendor
                    log.warn(message)
                    print(_yellow(message))
                os.mkdir(vendor_safestr)

            for fst in fsts[vendor]:
                # Copy the .fst
                fst_str = str(fst)
                message = "Copying %s to %s"
                log.debug(message % (fst_str, vendor))
                print(message % (_blue(fst_str), _green(vendor)))
                shutil.copy2(fst_str, vendor)

                # Copy the .nfo
                nfo = fst.with_suffix('.nfo')
                nfo_str = str(nfo)
                message = "Copying %s to %s"
                log.debug(message % (nfo_str, vendor))
                print(message % (_blue(nfo_str), _green(vendor)))
                shutil.copy2(nfo_str, vendor)
        # endregion
    # endregion

    # Success!
    print(
        _green("Finished creating database, copy 'Effects' and 'Generators'"
               "folders to %s to see them in FL." % str(fl_plugin_db_dir.parent)))

def main():
    if not sys.platform.startswith('win32'):
        raise EnvironmentError("This script is supposed to be run only on Windows.")

    # Argparse setup
    arg_parser = argparse.ArgumentParser(prog=FL_PLUGINDB_ORGANISER,
                                         description=__doc__)
    arg_parser.add_argument("output",
                            help="pathlib.Path to output database folders")
    arg_parser.add_argument("--log", '-l',
                            help="Location to output log file to, defaults "
                                 "to ./%s.log" % str(FL_PLUGINDB_ORGANISER))
    arg_parser.add_argument("--no-color",
                            action='store_true',
                            help="Disable colored output, necessary if you "
                                 "haven't installed ansicolors")

    args = arg_parser.parse_args()
    output_dir = None
    if args.output == '.':
        output_dir = pathlib.Path.cwd()
    else:
        output_dir = pathlib.Path(args.output)

    # Logging setup (log file is appended to on every run)
    default_log_name = "%s.log" % FL_PLUGINDB_ORGANISER
    default_log_location = "%s/%s" % (os.getcwd(), default_log_name)
    log_file = args.log if args.log else default_log_location

    logging.basicConfig(level=logging.DEBUG,
                        filename=log_file,
                        format='%(levelname)-8s %(message)s')

    log = logging.getLogger()
    log.setLevel(logging.CRITICAL)

    fl_plugin_db_organiser(output_dir, log, args.no_color)
