"""
Checks the installed serverjar for updates
"""

import os
from pathlib import Path
from rich.console import Console

from src.utils.console_output import rich_print_error
from src.serverjar.serverjar_paper_velocity_waterfall import serverjar_papermc_check_update, serverjar_papermc_update
from src.serverjar.serverjar_purpur import serverjar_purpur_check_update, serverjar_purpur_update
from src.handlers import handle_server


def get_installed_server_jar_file() -> str:
    """
    Gets the file name of the installed server jar

    :param config_values: Configuration values from pluGET config

    :returns: Full file name of installed server jar
    """

    file_list_server_root = handle_server.active_server.list_server_root()

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

    :returns: None
    """
    file_server_jar_full_name = get_installed_server_jar_file()
    if file_server_jar_full_name == None:
        # print error and exit function
        rich_print_error("Error: Serverjar couldn't be found")
        return None

    # TODO: Add other serverjars here
    # Paper / Velocity / Waterfall
    if "paper" in file_server_jar_full_name or \
        "waterfall" in file_server_jar_full_name or \
        "velocity" in file_server_jar_full_name:
        serverjar_papermc_check_update(file_server_jar_full_name)

    # Purpur
    elif "purpur" in file_server_jar_full_name:
        serverjar_purpur_check_update(file_server_jar_full_name)

    else:
        rich_print_error(f"[not bold]Error: [bright_magenta]{file_server_jar_full_name} [bright_red]isn't supported")

    return None


def update_installed_server_jar(server_jar_version: str="latest") -> None:
    """
    Handles the updating of the installed server jar

    :returns: None
    """
    file_server_jar_full_name = get_installed_server_jar_file()
    if file_server_jar_full_name == None:
        # print error and exit function
        rich_print_error("Error: Serverjar couldn't be found")
        return None

    # finding path which is used for deleting old server jar
    path_server_root = handle_server.active_server.root_path

    server_jar_path = f"{path_server_root}/{file_server_jar_full_name}"
    rich_console = Console()
    download_successfull = False
    # TODO: Add other serverjars here
    # Paper / Velocity / Waterfall
    if "paper" in file_server_jar_full_name or \
        "waterfall" in file_server_jar_full_name or \
        "velocity" in file_server_jar_full_name:
        download_successfull = serverjar_papermc_update(server_jar_version, None, file_server_jar_full_name, None)

    # Purpur
    elif "purpur" in file_server_jar_full_name:
        download_successfull = serverjar_purpur_update(server_jar_version, None, file_server_jar_full_name)

    else:
        rich_print_error(f"[not bold]Error: [bright_magenta]{file_server_jar_full_name} [bright_red]isn't supported")

    # remove old serverjar when the serverjar was sucessfully updated
    if download_successfull is True:
        handle_server.active_server.delete_server_jar(server_jar_path)
        rich_console.print(
            "    [not bold][bright_green]Deleted old server file [cyan]→ [white]" + 
            f"{file_server_jar_full_name}"
        )

    return None
