"""
Removes the specified plugin file from the ./plugins folder
"""

import os
import re
from pathlib import Path
from rich.console import Console
from src.utils.console_output import rich_print_error
from src.handlers import handle_server


def delete_plugin(plugin_name: str) -> None:
    """
    Deletes the specific plugin file

    :param plugin_name: Name of plugin file to delete

    :returns: None
    """
    rich_console = Console()
    handle_server.active_server.create_connection()
    plugin_list = handle_server.active_server.list_plugins()
    for plugin_file in plugin_list:
        # skip all other plugins
        if not re.search(plugin_name, plugin_file, re.IGNORECASE):
            continue

        try:
            handle_server.active_server.delete_plugin(plugin_file)
            rich_console.print(f"[not bold][bright_green]Successfully removed: [bright_magenta]{plugin_file}")
        except:
            rich_print_error(f"[not bold]Error: Couldn't remove [bright_magenta]{plugin_file}")
    handle_server.active_server.close_connection()
    return None
