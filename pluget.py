#!/usr/bin/env python3
"""Handles the main function and the argument passing for the whole pluGET program.

This module serves as the entry point for the application, processing command-line
arguments and delegating execution to the appropriate handlers.
"""

import sys
import argparse
from typing import Optional, Dict, Any

from src.handlers.handle_config import check_config, validate_config
from src.utils.console_output import (
    rename_console_title,
    clear_console,
    print_logo,
    print_console_logo,
)
from src.utils.utilities import (
    check_requirements,
    api_test_spiget,
    check_for_pluGET_update,
)
from src.handlers.handle_input import handle_input


def main() -> None:
    """Main execution function.

    Parses arguments, initializes configuration, performs checks, and starts
    the interactive or command-based session.
    """
    parser = argparse.ArgumentParser(
        description="Arguments for pluGET",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "mode", help="Mode (install/update/etc.)", nargs="?", default=None
    )
    parser.add_argument(
        "object", help="Object/Plugin Name", nargs="?", default=None
    )
    parser.add_argument("version", help="Version", nargs="?", default=None)
    parser.add_argument(
        "--no-confirmation",
        action="store_true",
        help="Skip confirmation messages",
    )
    
    # Type hinting for argparse results
    args_namespace = parser.parse_args()
    args: Dict[str, Any] = vars(args_namespace)

    rename_console_title()
    check_config()
    validate_config()
    api_test_spiget()
    check_requirements()

    mode: Optional[str] = args.get("mode")
    obj: Optional[str] = args.get("object")
    version: Optional[str] = args.get("version")
    no_confirmation: bool = args.get("no_confirmation", False)

    if mode is not None and obj is not None:
        # Arguments were used so call the handle_input function to get the right function call
        print_console_logo()
        check_for_pluGET_update()
        handle_input(
            input_command=mode,
            input_selected_object=obj,
            input_parameter=version,
            no_confirmation=no_confirmation,
            arguments_from_console=True,
        )
    else:
        # No arguments were used so start pluGET console
        clear_console()
        print_logo()
        check_for_pluGET_update()
        handle_input()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
