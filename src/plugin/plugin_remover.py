"""
Removes the specified plugin file from the ./plugins folder
"""

import os
import re
from pathlib import Path
from rich.console import Console

from src.handlers.handle_config import config_value
from src.utils.console_output import rich_print_error
from src.handlers.handle_sftp import sftp_create_connection, sftp_list_all
from src.handlers.handle_ftp import ftp_create_connection, ftp_list_all


def delete_plugin(plugin_name: str) -> None:
    """
    Deletes the specific plugin file

    :param plugin_name: Name of plugin file to delete

    :returns: None
    """
    config_values = config_value()
    rich_console = Console()
    match config_values.connection:
        case "sftp":
            connection = sftp_create_connection()
            plugin_list = sftp_list_all()
        case "ftp":
            connection = ftp_create_connection()
            plugin_list = ftp_list_all()
        case "local":
            plugin_list = os.listdir(config_values.path_to_plugin_folder)
    for plugin_file in plugin_list:
        # skip all other plugins
        if not re.search(plugin_name, plugin_file, re.IGNORECASE):
            continue

        try:
            match config_values.connection:
                case "sftp":
                    plugin_path = f"{config_values.remote_plugin_folder_on_server}/{plugin_file}"
                    connection = sftp_create_connection()
                    connection.remove(plugin_path)
                case "ftp":
                    plugin_path = f"{config_values.remote_plugin_folder_on_server}/{plugin_file}"
                    connection = ftp_create_connection()
                    connection.delete(plugin_path)
                case "local":
                    pluginPath = Path(f"{config_values.path_to_plugin_folder}/{plugin_file}")
                    os.remove(pluginPath)
            rich_console.print(f"[not bold][bright_green]Successfully removed: [bright_magenta]{plugin_file}")
        except:
            rich_print_error(f"[not bold]Error: Couldn't remove [bright_magenta]{plugin_file}")
    return None
