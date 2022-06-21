"""
Handles the plugin checking and updating
"""

import os
import re
from pathlib import Path
from rich.progress import track
from rich.table import Table
from rich.console import Console


from src.handlers.handle_config import config_value
from src.handlers.handle_sftp import sftp_create_connection, sftp_validate_file_attributes, sftp_list_all
from src.handlers.handle_ftp import ftp_create_connection, ftp_validate_file_attributes, ftp_list_all
from src.utils.utilities import api_do_request

class Plugin():
    """
    Create plugin class to store installed plugins inside it
    """
    def __init__(
        self,
        plugin_file_name : str,
        plugin_name : str,
        plugin_file_version : str,
        plugin_latest_version : str,
        plugin_is_outdated : bool,
        plugin_repository : str,
        plugin_repository_data : list
        ) -> None:

        self.plugin_file_name = plugin_file_name
        self.plugin_name = plugin_name
        self.plugin_file_version = plugin_file_version
        self.plugin_latest_version = plugin_latest_version
        self.plugin_is_outdated = plugin_is_outdated
        self.plugin_repository = plugin_repository
        self.plugin_repository_data = plugin_repository_data


    @staticmethod
    def create_plugin_list() -> list:
        """
        Creates a global array list to store plugins
        """
        global INSTALLEDPLUGINLIST
        INSTALLEDPLUGINLIST = []
        return INSTALLEDPLUGINLIST


    @staticmethod
    def add_to_plugin_list(
        plugin_file_name: str,
        plugin_name : str,
        plugin_file_version : str,
        plugin_latest_version : str,
        plugin_is_outdated : bool,
        plugin_repository : str,
        plugin_repository_data : list
        ) -> None:
        """
        Adds a plugin to global installed plugin lists
        """
        INSTALLEDPLUGINLIST.append(Plugin(
            plugin_file_name, 
            plugin_name, 
            plugin_file_version, 
            plugin_latest_version, 
            plugin_is_outdated, 
            plugin_repository, 
            plugin_repository_data
            ))
        return None


def get_plugin_file_name(plugin_full_name : str) -> str:
    """
    Finds the full plugin name of the given string
    Example LuckPerms-5.4.30.jar -> Luckperms

    :param plugin_full_name: Full filename of plugin

    :returns: Full plugin name
    """
    plugin_full_name2 = plugin_full_name
    # find number.jar
    plugin_file_version = re.search(r'([\d.]+[.jar]+)', plugin_full_name2)
    try:
        plugin_file_version_full = plugin_file_version.group()
    except AttributeError:
        plugin_file_version_full = plugin_file_version
    # remove number from plugin name
    plugin_name_only = plugin_full_name2.replace(plugin_file_version_full, '')
    # remove - from plugin name
    plugin_name_only = re.sub(r'(\-$)', '', plugin_name_only)
    # remove -v from plugin name
    plugin_name_only = re.sub(r'(\-v$)', '', plugin_name_only)
    return plugin_name_only


def get_plugin_file_version(plugin_full_name : str) -> str:
    """
    Gets the version of the plugin

    :param plugin_full_name: Full filename of plugin

    :returns: Version of plugin as string
    """
    plugin_file_version = re.search(r'([\d.]+[.jar]+)', plugin_full_name)
    plugin_file_version = plugin_file_version.group()
    plugin_file_version = plugin_file_version.replace('.jar', '')
    if plugin_file_version.endswith('.'):
        print("get_plugin_file_version endswith .")
        #plugin_file_version = eggCrackingJar(plugin_full_name, 'version')
    return plugin_file_version


def get_latest_spigot_plugin_version(plugin_id : str) -> str:
    """
    Gets the latest spigot plugin version
    
    :param plugin_id: Plugin Spigot ID

    :returns: Name of the latest update
    """
    url = f"https://api.spiget.org/v2/resources/{plugin_id}/versions/latest"
    latest_update_search = api_do_request(url)
    return str(latest_update_search["name"])


def create_plugin_version_tuple(plugin_version_string : str) -> tuple:
    """
    Create a tuple of all version numbers

    :param plugin_version_string: Plugin Version

    :returns: Tuple of all version numbers
    """
    return tuple(map(int, (plugin_version_string.split("."))))


def get_plugin_version_without_letters(plugin_version_string : str) -> str:
    """
    Returns the version without letters from the plugin version

    :param plugin_version_string: Plugin Version
    
    :returns: Plugin version without letters
    """
    return re.sub(r'([A-Za-z]*)', '', plugin_version_string)


def compare_plugin_version(plugin_latest_version : str, plugin_file_version : str) -> bool:
    """
    Check if plugin version is outdated

    :param plugin_latest_version: Latest available plugin version
    :param plugin_file_version: Installed plugin version
    
    :returns: bool if plugin version is outdated
    """
    try:
        plugin_version_tuple = create_plugin_version_tuple(
            get_plugin_version_without_letters(plugin_file_version))
        plugin_latest_version_tuple = create_plugin_version_tuple(
            get_plugin_version_without_letters(plugin_latest_version))
    except ValueError:
        return False
    if plugin_version_tuple < plugin_latest_version_tuple:
        return True
    else:
        return False


def check_installed_plugins(input_selected_object : str="all", input_parameter : str=None) -> None:
    """
    Gets installed plugins and checks it against the apis if there are updates for the plugins available

    :param input_selected_object: Which plugin should be checked
    :param input_parameter: Optional parameters

    :returns: None
    """
    config_values = config_value()
    Plugin.create_plugin_list()
    match config_values.connection:
        case "sftp":
            connection = sftp_create_connection()
            plugin_list = sftp_list_all(connection)
        case "ftp":
            connection = ftp_create_connection()
            plugin_list = ftp_list_all(connection)
        case _:
            plugin_folder_path = config_values.path_to_plugin_folder
            plugin_list = os.listdir(plugin_folder_path)

    plugin_count = plugins_with_udpates = 0
    # create simple progress bar from rich
    for plugin_file in track(plugin_list, description="[cyan]Checking...", transient=True, style="bright_yellow"):
        plugin_attributes = True
        match config_values.connection:
            case "sftp":
                plugin_attributes = sftp_validate_file_attributes(
                    connection, f"{config_values.remote_plugin_folder_on_server}/{plugin}"
                    )
            case "ftp":
                plugin_attributes = ftp_validate_file_attributes(
                    connection, f"{config_values.remote_plugin_folder_on_server}/{plugin}"
                    )
            case _:
                if not os.path.isfile(Path(f"{plugin_folder_path}/{plugin_file}")):
                    plugin_attributes = False
                if not re.search(r'.jar$', plugin_file):
                    plugin_attributes = False
        # skip plugin if no attributes were found
        if plugin_attributes == False:
            continue

        plugin_file_name = get_plugin_file_name(plugin_file)
        # supports command 'check pluginname' and skip the checking of every other plugin to speed things up a bit
        if input_selected_object != "all" and input_selected_object != "*":
            if not re.search(input_selected_object, plugin_file_name, re.IGNORECASE):
                continue

        plugin_file_version = get_plugin_file_version(plugin_file)
        # check repository of plugin
        plugin_spigot_id = search_plugin_spigot(plugin_file, plugin_file_name, plugin_file_version) # plugin_spigot_id isn't needed
        # TODO add more plugin repositories here

        # plugin wasn't found and not added to global plugin list so add 
        if plugin_file not in INSTALLEDPLUGINLIST[-1].plugin_file_name:
            print(f"skipped {plugin_file}")
            Plugin.add_to_plugin_list(plugin_file, plugin_file_name, plugin_file_version, 'N/A', False, 'N/A', ())
        if INSTALLEDPLUGINLIST[-1].plugin_is_outdated == True:
            plugins_with_udpates += 1
        plugin_count += 1

    # print rich table of found plugins and result
    rich_table = Table(box=None)
    rich_table.add_column("No.", justify="right", style="cyan", no_wrap=True)
    rich_table.add_column("Name", style="bright_magenta")
    rich_table.add_column("Installed V.", justify="right", style="bright_green")
    rich_table.add_column("Latest V.", justify="right", style="green")
    rich_table.add_column("Update available", justify="left", style="white")
    rich_table.add_column("Repository", justify="left", style="white")
    # start counting at 1 for all my non-programming friends :)
    i = 1
    for plugin in INSTALLEDPLUGINLIST:
        rich_table.add_row(
            str(i), 
            plugin.plugin_name, 
            plugin.plugin_file_version, 
            plugin.plugin_latest_version, 
            str(plugin.plugin_is_outdated), 
            plugin.plugin_repository
        )
        i += 1

    rich_console = Console()
    rich_console.print(rich_table)
    if plugins_with_udpates != 0:
        rich_console.print(
        "[not bold][bright_yellow]Plugins with available updates: [bright_green]" +
        f"{plugins_with_udpates}[bright_yellow]/[bright_magenta]{plugin_count}"
            )
    else:
        rich_console.print(f"[bright_green]All found plugins are on the newest version!")
    return None


def search_plugin_spigot(plugin_file : str, plugin_file_name : str, plugin_file_version : str) -> int:
    """
    Search the spigot api for the installed plugin and add it to the installed plugin list

    :param plugin_file: Full file name of plugin
    :param plugin_file_name: Name of plugin file
    :param plugin_file_version: Version of plugin file

    :returns: Plugin ID of Spigot Plugin
    """
    url = f"https://api.spiget.org/v2/search/resources/{plugin_file_name}?field=name&sort=-downloads"
    plugin_list = api_do_request(url)
    plugin_file_version2 = plugin_file_version
    for i in range(3):
        if i == 1:
            plugin_file_version2 = re.sub(r'(\-\w*)', '', plugin_file_version)
        if i == 2:
            """
            plugin_name_in_yml = eggCrackingJar(plugin_file, 'name')
            url = f"https://api.spiget.org/v2/search/resources/{plugin_name_in_yml}?field=name&sort=-downloads"
            try:
                plugin_list = api_do_request(url)
            except ValueError:
                continue
            """

            #plugin_file_version = plugin_file_version2 # ?

        for plugin in plugin_list:
            plugin_id = plugin["id"]
            url2 = f"https://api.spiget.org/v2/resources/{plugin_id}/versions?size=100&sort=-name"
            try:
                plugin_versions = api_do_request(url2)
            except ValueError:
                continue
            for updates in plugin_versions:
                update_version_name = updates["name"]
                if plugin_file_version2 in update_version_name:
                    #spigot_update_id = updates["id"]
                    plugin_latest_version = get_latest_spigot_plugin_version(plugin_id)
                    plugin_is_outdated = compare_plugin_version(plugin_latest_version, update_version_name)
                    Plugin.add_to_plugin_list(
                        plugin_file,
                        plugin_file_name,
                        plugin_file_version,
                        plugin_latest_version,
                        plugin_is_outdated,
                        "spigot",
                        (plugin_id)
                    )
                    return plugin_id
    return None
