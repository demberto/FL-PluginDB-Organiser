#############################
# FL Plugin DB Categorizer  #
#                           #
# Author: @demberto         #
#                           #
#############################



__doc__ = "Reads plugin database files (.nfo) created by FL Studio and \
           reorganizes them into folders based on plugin vendor names."

import os
import sys
import argparse
import logging
import shutil
import configparser
from pathlib import Path
from typing import List, Dict

# Argparse setup
arg_parser = argparse.ArgumentParser(description=__doc__)
arg_parser.add_argument("output", help="Path to output database folders")

# Logging setup (log file is appended to on every run)
logging.basicConfig(level=logging.DEBUG,
                    filename=sys.argv[0] + '.log',
                    format='%(levelname)-8s %(message)s')

console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)

def main(output_dir: Path):
    # Init
    if output_dir == Path('.'):
        output_dir = Path.cwd()
    os.chdir(output_dir)
    GENERATORS = output_dir / "Generators"
    EFFECTS = output_dir / "Effects"
    
    # Create 'Generators' and 'Effects' folders
    log.info(f"Creating 'Effects' folder")
    EFFECTS.mkdir(exist_ok=True)

    log.info(f"Creating 'Generators' folder")
    GENERATORS.mkdir(exist_ok=True)

    # Gather .nfo/.fst locations
    log.info("Finding existing database locations...")

    FL_PLUGIN_DB_DIR = Path.expanduser(
        Path(
            "~/Documents/Image-Line/FL Studio/Presets/Plugin database/Installed/"
        )
    )
    VST2_EFFECT_DB_DIR = FL_PLUGIN_DB_DIR / "Effects/VST"
    VST3_EFFECT_DB_DIR = FL_PLUGIN_DB_DIR / "Effects/VST3"
    VST2_GENERATOR_DB_DIR = FL_PLUGIN_DB_DIR / "Generators/VST"
    VST3_GENERATOR_DB_DIR = FL_PLUGIN_DB_DIR / "Generators/VST3"

    config_parser = configparser.ConfigParser()

    # Discover .nfos, warn user of any missing folders.
    for folder in (VST2_EFFECT_DB_DIR, VST2_GENERATOR_DB_DIR,
                VST3_EFFECT_DB_DIR, VST3_GENERATOR_DB_DIR):

        fsts: Dict[Path, List[Path]] = {}   # Vendor to .fst mapping
        nfos: List[Path] = []   # Temporary list of .nfo files

        log.info(f"Scanning {str(folder)}")

        if folder.is_dir():
            nfos.extend(tuple(folder.glob('*.nfo')))
        else:
            log.warn(f"{str(folder)} doesn't exist or isn't a folder")

        # Read vendor names from each .nfo and populate fsts.
        log.info("Finding vendor names")
        for nfo in nfos:
            stream = open(nfo).read()
            config_string = "[dummy_section]\n" + stream
            config_parser.read_string(config_string)

            dummy_section = config_parser['dummy_section']
            vendor = dummy_section.get('ps_file_vendorname_0')

            if vendor:
                fst = nfo.with_suffix('.fst')
                if fst.is_file():
                    vendor_path = Path(vendor)
                    if not vendor_path in fsts:
                        fsts[vendor_path] = []
                    fsts[vendor_path].append(fst)
                else:
                    log.warn(f"No corresponding .fst found for {str(nfo)}")
            else:
                log.warn(f"Couldn't find vendor name from {str(nfo)}")

        vendors = [str(vendor_path) for vendor_path in fsts.keys()]
        log.info(f"Found {len(vendors)} vendors: ", vendors)

        # Create folders with vendor names and copy .fst to them
        if folder in (VST2_GENERATOR_DB_DIR, VST3_GENERATOR_DB_DIR):
            os.chdir(GENERATORS)
        else:
            os.chdir(EFFECTS)

        log.info(f"Creating new plugin database at {os.getcwd()}")
        for vendor in fsts.keys():
            vendor_str = str(vendor)

            if not vendor.is_dir():
                log.debug(f"Creating vendor folder {vendor_str}")
                vendor.mkdir()

            for fst in fsts[vendor]:
                log.debug(f"Copying {str(fst)} to '{vendor_str}'")
                shutil.copy2(fst, vendor)

                nfo = fst.with_suffix('.nfo')
                log.debug(f"Copying {str(nfo)} to '{vendor_str}'")
                shutil.copy2(nfo, vendor)

    # Sucess
    print(f"Finished creating database, copy 'Effects' and 'Generators' \
    folders to {str(FL_PLUGIN_DB_DIR.parent)} to see them in FL. \
    Don't forget to take backup first :)")

if __name__ == '__main__':
    args = arg_parser.parse_args()
    output_dir = Path(args.output)
    main(output_dir)