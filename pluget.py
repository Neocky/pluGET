#!/usr/bin/env python
"""
Handles the main function and the argument passing for the whole pluGET program
"""

import sys
import argparse

# check if folder 'src' is accessible with all modules needed and if not exit
try:
    from src.handlers.handle_config import check_config, validate_config
    from src.utils.console_output import rename_console_title, clear_console, print_logo, print_console_logo
    from src.utils.utilities import check_requirements, api_test_spiget, check_for_pluGET_update
    from src.handlers.handle_input import handle_input
except TypeError:
    print("Folder 'src' not found in the directory or missing files or broken functions detected! \
        \nPlease redownload the files from here: https://www.github.com/Neocky/pluGET")
    sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arguments for pluGET",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("mode", help="Mode (install/update/etc.)", nargs='?', default=None)
    parser.add_argument("object", help="Object/Plugin Name", nargs='?', default=None)
    parser.add_argument("version", help="Version", nargs='?', default=None)
    parser.add_argument("--no-confirmation", action="store_true", help="Skip confirmation messages")
    args = vars(parser.parse_args())

    rename_console_title()
    check_config()
    validate_config()
    api_test_spiget()
    check_requirements()

    if args["mode"] is not None and args["object"] is not None:
        # arguments were used so call the handle_input function to get the right function call
        print_console_logo()
        check_for_pluGET_update()
        handle_input(args["mode"], args["object"], args["version"], args["no_confirmation"], arguments_from_console=True)
    else:
        # no arguments were used so start pluGET console
        clear_console()
        print_logo()
        check_for_pluGET_update()
        handle_input()
