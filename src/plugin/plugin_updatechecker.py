"""
Handles the plugin checking and updating
"""

import os
import re
from pathlib import Path
from rich.progress import track


from src.handlers.handle_config import config_value
from src.utils.utilities import api_do_request

class plugin():
    """
    Create plugin class to store installed plugins inside it
    """
    def __init__(self, plugin_name, plugin_file_version) -> None:
        self.plugin_name = plugin_name
        self.plugin_file_version = plugin_file_version


    @staticmethod
    def create_plugin_list() -> list:
        """
        Creates a global array list to store plugins
        """
        global INSTALLEDPLUGINLIST
        INSTALLEDPLUGINLIST = []
        return INSTALLEDPLUGINLIST


    @staticmethod
    def add_to_plugin_list(plugin_name, plugin_file_version) -> None:
        """
        Adds a plugin to global installed plugin lists
        """
        INSTALLEDPLUGINLIST.append(plugin(plugin_name, plugin_file_version))
        return None

    @staticmethod
    def get_plugin_list_length() -> int:
        """
        Returns the lenght of the plugin list
        """
        return len(INSTALLEDPLUGINLIST)




#plugin.create_plugin_list()
#plugin.add_to_plugin_list("test2", 12345)
#for i in INSTALLEDPLUGINLIST: print(i.plugin_name)
#print(plugin.get_plugin_list_length())

def get_plugin_file_name(plugin_full_name) -> str:
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


def get_plugin_file_version(plugin_full_name) -> str:
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


def get_latest_spigot_plugin_version(plugin_id) -> str:
    """
    Gets the latest spigot plugin version
    
    :param plugin_id: Plugin Spigot ID

    :returns: Name of the latest update
    """
    url = f"https://api.spiget.org/v2/resources/{plugin_id}/versions/latest"
    latest_update_search = api_do_request(url)
    return str(latest_update_search["name"])


def create_plugin_version_tuple(plugin_version_string) -> tuple:
    """
    Create a tuple of all version numbers

    :param plugin_version_string: Plugin Version

    :returns: Tuple of all version numbers
    """
    return tuple(map(int, (plugin_version_string.split("."))))


def get_plugin_version_without_letters(plugin_version_string) -> str:
    """
    Returns the version without letters from the plugin version

    :param plugin_version_string: Plugin Version
    
    :returns: Plugin versioon without letters
    """
    return re.sub(r'([A-Za-z]*)', '', plugin_version_string)


def compare_plugin_version(plugin_latest_version, plugin_file_version) -> bool:
    """
    Check if plugin version is outdated

    :param plugin_latest_version: Latest available plugin version
    :param plugin_file_version: Installed plugin version
    
    :returns: Bool if plugin version is outdated
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


def check_installed_plugins(input_selected_object="all", input_parameter=None) -> None:
    """
    Gets installed plugins and checks it against the apis if there are updates for the plugins available

    :param input_selected_object: Which plugin should be checked
    :param input_parameter: Optional parameters

    :returns: None
    """
    config_values = config_value()
    plugin.create_plugin_list()
    match config_values.connection:
        case "sftp":
            # TODO add sftp adn ftp support
            #connection = createSFTPConnection()
            #pluginList = sftp_listAll(connection)
            print("sftp list all")
        case "ftp":
            print("ftp list all")
        case _:
            plugin_folder_path = config_values.path_to_plugin_folder
            plugin_list = os.listdir(plugin_folder_path)

    # create simple progress bar from rich
    for plugin_file in track(plugin_list, description="[cyan]Checking...", transient=True, style="bright_yellow"):
        plugin_no_attributes = False
        match config_values.connection:
            case "sftp":
                #plugin_attributes = sftp_validateFileAttributes(connection, f"config_values.remote_plugin_folder_on_server}/{plugin}")
                print("sftp check_installed_plugins")

            case "ftp":
                #plugin_attributes = ftp_validateFileAttributes(connection, f"config_values.remote_plugin_folder_on_server}/{plugin}")
                print("ftp check_installed_plugins")
            case _:
                if not os.path.isfile(Path(f"{plugin_folder_path}/{plugin_file}")):
                    plugin_no_attributes = True
                if not re.search(r'.jar$', plugin_file):
                    plugin_no_attributes = True
        # skip plugin if no attributes were found
        if plugin_no_attributes == True:
            continue

        plugin_file_name = get_plugin_file_name(plugin_file)
        plugin_file_version = get_plugin_file_version(plugin_file)
        # check repository of plugin
        plugin_spigot_id = search_plugin_spigot(plugin_file, plugin_file_name, plugin_file_version)
        # TODO add more plugin repositories here
        print(plugin_file_name)
        print(plugin_file_version)
        print(plugin_spigot_id)




def search_plugin_spigot(plugin_file, plugin_file_name, plugin_file_version) -> int:
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
                    spigot_update_id = updates["id"]
                    plugin_latest_version = get_latest_spigot_plugin_version(plugin_id)
                    plugin_is_outdated = compare_plugin_version(plugin_latest_version, update_version_name)
                    #addToPluginList(plugin_file, plugin_id, spigot_update_id,  plugin_latest_version , plugin_is_outdated)
                    return plugin_id, plugin_is_outdated

    #plugin_id = spigot_update_id = plugin_latest_version = plugin_is_outdated = None
            #addToPluginList(plugin_file, plugin_id, spigot_update_id,  plugin_latest_version , plugin_is_outdated)
    return None
