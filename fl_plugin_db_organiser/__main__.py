"""Entry-point of script. Creates a logger and argument parser"""

import argparse
import logging
import os
import pathlib
import sys

from . import fl_plugin_db_organiser

FL_PLUGINDB_ORGANISER = "fl-plugindb-organizer"

if __name__ == '__main__':
    if not sys.platform.startswith('win32'):
        raise EnvironmentError("This script is supposed to be run only on Windows.")

    # Argparse setup
    arg_parser = argparse.ArgumentParser(prog=FL_PLUGINDB_ORGANISER,
                                         description=__doc__)
    arg_parser.add_argument("output",
                            help="Path to output database folders")
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
