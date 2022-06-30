"""
Checks the installed serverjar for updates
"""

import os
from rich.console import Console

from src.utils.console_output import rich_print_error
from src.handlers.handle_config import config_value
from src.handlers.handle_sftp import sftp_create_connection, sftp_list_files_in_server_root
from src.handlers.handle_ftp import ftp_create_connection, ftp_list_files_in_server_root


def get_installed_server_jar_file(config_values) -> str:
    """
    Gets the file name of the installed server jar

    :param config_values: Configuration values from pluGET config

    :returns: Full file name of installed server jar
    """
    match config_values.connection:
        case "sftp":
            connection = sftp_create_connection()
            file_list_server_root = sftp_list_files_in_server_root(connection)
        case "ftp":
            connection = ftp_create_connection()
            file_list_server_root = ftp_list_files_in_server_root(connection)
        case _:
            file_list_server_root = os.path.dirname(config_values.path_to_plugin_folder)
            file_list_server_root = os.listdir(file_list_server_root)

    file_server_jar_full_name = None
    try:
        for file in file_list_server_root:
            try:
                if ".jar" in file:
                    file_server_jar_full_name = file
                    break
            except TypeError:
                continue
    except TypeError:
        rich_print_error("Error: Serverjar couldn't be found")
        return None
    return file_server_jar_full_name


def check_update_available_installed_server_jar() -> None:
    """
    Handles the checking of available updates of the installed server jar

    :params: None
    """
    config_values = config_value()
    rich_console = Console()
    file_server_jar_full_name = get_installed_server_jar_file(config_values)
    if file_server_jar_full_name == None:
        # print error and exit function
        rich_print_error("Error: Serverjar couldn't be found")
        return None
    
    rich_console.print(f"[not bold][cyan]Checking: [bright_magenta]{file_server_jar_full_name}")

    # TODO: Add other serverjars here
    if "paper" in file_server_jar_full_name:
        print("paper check update")
        print(file_server_jar_full_name)

    else:
        rich_print_error(f"{file_server_jar_full_name} isn't supported")
