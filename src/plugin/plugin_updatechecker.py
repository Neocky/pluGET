"""
Handles the plugin checking and updating
"""

import os
import re
import io
from pathlib import Path
import zipfile
from rich.progress import track
from rich.table import Table
from rich.console import Console
from urllib.error import HTTPError
from zipfile import ZipFile

from src.handlers.handle_config import config_value
from src.handlers.handle_sftp import sftp_create_connection, sftp_download_file, sftp_validate_file_attributes, sftp_list_all
from src.handlers.handle_ftp import ftp_create_connection, ftp_download_file, ftp_validate_file_attributes, ftp_list_all
from src.plugin.plugin_downloader import get_specific_plugin_spiget, get_download_path
from src.utils.console_output import rich_print_error
from src.utils.utilities import api_do_request, create_temp_plugin_folder, remove_temp_plugin_folder


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


def get_plugin_file_name(plugin_full_name: str) -> str:
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


def get_plugin_file_version(plugin_full_name: str) -> str:
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
        plugin_file_name, plugin_file_version = egg_cracking_jar(plugin_full_name)
    return plugin_file_version


def get_latest_plugin_version_spiget(plugin_id : str) -> str:
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


def ask_update_confirmation(input_selected_object : str) -> bool:
    """
    Prints confirmation message of plugins which get updated and ask for confirmation

    :param input_selected_object: Command line input

    :returns: True or False if plugins should be udpated
    """
    rich_console = Console()
    rich_console.print("Selected plugins with available Updates:")
    for plugin_file in INSTALLEDPLUGINLIST:
        if plugin_file.plugin_is_outdated == False:
            continue
        if input_selected_object != "all" and input_selected_object != "*":
            if re.search(input_selected_object, plugin_file.plugin_file_name, re.IGNORECASE):
                rich_console.print(f"[not bold][bright_magenta]{plugin_file.plugin_name}", end=' ')
                break
        rich_console.print(f"[not bold][bright_magenta]{plugin_file.plugin_name}", end=' ')

    rich_console.print()
    update_confirmation = input("Update these plugins [y/n] ? ")
    if str.lower(update_confirmation) != "y":
        rich_print_error("Aborting the update process")
        return False
    return True


def egg_cracking_jar(plugin_file_name: str) -> str:
    """
    Opens the plugin file as an archive and searches the plugin.yml file for the name and version entry

    :param plugin_file_name: Filename of the plugin which should be openend

    :returns: Plugin name in plugin.yml file
    :returns: Plugin version in plugin.yml file
    """
    config_values = config_value()
    match config_values.connection:
        case "sftp":
            path_temp_plugin_folder = create_temp_plugin_folder()
            connection = sftp_create_connection()
            sftp_download_file(connection, plugin_file_name)
            path_plugin_jar = Path(f"{path_temp_plugin_folder}/{plugin_file_name}")
        case "ftp":
            path_temp_plugin_folder = create_temp_plugin_folder()
            connection = ftp_create_connection()
            ftp_download_file(connection, plugin_file_name)
            path_plugin_jar = Path(f"{path_temp_plugin_folder}/{plugin_file_name}")
        case _:
            path_plugin_folder = config_values.path_to_plugin_folder
            path_plugin_jar = Path(f"{path_plugin_folder}/{plugin_file_name}")
    
    # later used to escape for-loop
    plugin_name = plugin_version = ""
    # open plugin if it is an archive and read plugin.yml line for line to find name & version
    try:
        with ZipFile(path_plugin_jar, "r") as plugin_jar:
            with io.TextIOWrapper(plugin_jar.open("plugin.yml", "r"), encoding="utf-8") as plugin_yml:
                for line in plugin_yml:
                    if plugin_name != "" and plugin_version != "":
                        break
                    if re.match(r"^\s*?name: ", line):
                        plugin_name = re.sub(r'^\s*?name: ', '', line)
                        plugin_name = plugin_name.replace("\n", "").replace("'", "").replace('"', "")

                    if re.match(r"^\s*?version: ", line):
                        plugin_version = re.sub(r'^\s*?version: ', "", line)
                        plugin_version = plugin_version.replace("\n", "").replace("'", "").replace('"', "")

    except FileNotFoundError:
        plugin_name = plugin_version = ""
    except KeyError:
        plugin_name = plugin_version = ""        
    except zipfile.BadZipFile:
        plugin_name = plugin_version = ""

    # remove temp plugin folder if plugin was downloaded from sftp/ftp server
    if config_values.connection != "local":
        remove_temp_plugin_folder()

    return plugin_name, plugin_version


def check_update_available_installed_plugins(input_selected_object: str, config_values: config_value) -> str:
    """
    Gets installed plugins and checks it against the apis if there are updates for the plugins available

    :param input_selected_object: Command line input (default: all)
    :param config_values: Config values from config file

    :returns: Count of plugins, Count of plugins with available updates
    """
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
                    connection, f"{config_values.remote_plugin_folder_on_server}/{plugin_file}"
                )
            case "ftp":
                plugin_attributes = ftp_validate_file_attributes(
                    connection, f"{config_values.remote_plugin_folder_on_server}/{plugin_file}"
                )
            case _:
                if not os.path.isfile(Path(f"{plugin_folder_path}/{plugin_file}")):
                    plugin_attributes = False
                if not re.search(r'.jar$', plugin_file):
                    plugin_attributes = False
        # skip plugin if no attributes were found to skip not valid plugin files
        if plugin_attributes == False:
            continue

        plugin_file_name = get_plugin_file_name(plugin_file)
        # supports command 'check pluginname' and skip the checking of every other plugin to speed things up a bit
        if input_selected_object != "all" and input_selected_object != "*":
            if not re.search(input_selected_object, plugin_file_name, re.IGNORECASE):
                continue

        plugin_file_version = get_plugin_file_version(plugin_file)
        # check repository of plugin
        plugin_spigot_id = search_plugin_spiget(plugin_file, plugin_file_name, plugin_file_version) # plugin_spigot_id isn't needed
        # TODO add more plugin repositories here

        # plugin wasn't found and not added to global plugin list so add
        try:
            if plugin_file not in INSTALLEDPLUGINLIST[-1].plugin_file_name:
                Plugin.add_to_plugin_list(plugin_file, plugin_file_name, plugin_file_version, 'N/A', False, 'N/A', ())
        except IndexError:
            Plugin.add_to_plugin_list(plugin_file, plugin_file_name, plugin_file_version, 'N/A', False, 'N/A', ())
        if INSTALLEDPLUGINLIST[-1].plugin_is_outdated == True:
            plugins_with_udpates += 1
        plugin_count += 1
    return plugin_count, plugins_with_udpates


def check_installed_plugins(input_selected_object : str="all", input_parameter : str=None) -> None:
    """
    Prints table overview of installed plugins with versions and available updates

    :param input_selected_object: Which plugin should be checked
    :param input_parameter: Optional parameters

    :returns: None
    """
    config_values = config_value()
    plugin_count, plugins_with_udpates = check_update_available_installed_plugins(input_selected_object, config_values)

    # print rich table of found plugins and result
    rich_table = Table(box=None)
    rich_table.add_column("No.", justify="right", style="cyan", no_wrap=True)
    rich_table.add_column("Name", style="bright_magenta")
    rich_table.add_column("Installed V.", justify="right", style="green")
    rich_table.add_column("Latest V.", justify="right", style="bright_green")
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
    rich_console.print()
    if plugins_with_udpates != 0:
        rich_console.print(
        "[not bold][bright_yellow]Plugins with available updates: [bright_green]" +
        f"{plugins_with_udpates}[bright_yellow]/[green]{plugin_count}"
            )
    else:
        rich_console.print(f"[bright_green]All found plugins are on the newest version!")
    return None


def update_installed_plugins(input_selected_object : str="all", no_confirmation : bool=False) -> None:
    """
    Checks if a plugin list exists and if so updates the selected plugins if there is an update available

    :param input_selected_object: Plugin name to update (use 'all' or '*' for everything)
    :param no_confirmation: Don't ask for confirmation if pluGET was called with param: --no-confirmation

    :returns: None
    """
    rich_console = Console()
    config_values = config_value()
    match config_values.connection:
        case "sftp":
            connection = sftp_create_connection()
        case "ftp":
            connection = ftp_create_connection()
    # if INSTALLEDPLUGINLIST was not previously filled by 'check' command call the command to fill plugin list
    try:
        if len(INSTALLEDPLUGINLIST) == 0:
            check_update_available_installed_plugins(input_selected_object, config_values)
    except NameError:
        check_update_available_installed_plugins(input_selected_object, config_values)

    # if argument 'all' was given recheck all plugins to avoid having only a few plugins from previously cached checks
    if input_selected_object == "all" or input_selected_object == "*":
        check_update_available_installed_plugins(input_selected_object, config_values)

    # skip confirmation message if pluGET was called with --no-confirmation
    if no_confirmation == False:
        if ask_update_confirmation(input_selected_object) == False:
            return None

    # used later for output as stats
    plugins_updated = plugins_skipped = 0

    #for plugin in track(INSTALLEDPLUGINLIST, description="[cyan]Updating...", transient=True, style="bright_yellow"):
    for plugin in INSTALLEDPLUGINLIST:
        # supports command 'update pluginname' and skip the updating of every other plugin to speed things up a bit
        if input_selected_object != "all" and input_selected_object != "*":
            if not re.search(input_selected_object, plugin.plugin_file_name, re.IGNORECASE):
                plugins_skipped += 1
                continue

        if plugin.plugin_is_outdated == False:
            plugins_skipped += 1
            continue

        rich_console.print(
            "\n [not bold][bright_white]● [bright_magenta]" +
            f"{plugin.plugin_name} [green]{plugin.plugin_file_version}" + \
            f" [cyan]→ [bright_green]{plugin.plugin_latest_version}"
        )

        plugins_updated += 1
        plugin_path = get_download_path(config_values)
        match config_values.connection:
            # local plugin folder
            case "local":
                match (plugin.plugin_repository):
                    case "spigot":
                        try:
                            get_specific_plugin_spiget(plugin.plugin_repository_data[0])
                        except HTTPError as err:
                            rich_print_error(f"HTTPError: {err.code} - {err.reason}")
                            plugins_updated -= 1
                        except TypeError:
                            rich_print_error(
                                f"Error: TypeError > Couldn't download new version. Is the file available on spigotmc?"
                            )
                            plugins_updated -= 1

                    case _:
                        rich_print_error("Error: Plugin repository wasn't found")
                        return None
                # don't delete files if they are downloaded to a seperate download path
                if config_values.local_seperate_download_path == False:
                    try:
                        os.remove(Path(f"{plugin_path}/{plugin.plugin_file_name}"))
                        rich_console.print(
                            "    [not bold][bright_green]Deleted old plugin file [cyan]→ [white]" + 
                            f"{plugin.plugin_file_name}"
                        )
                    except FileNotFoundError:
                        rich_print_error("Error: Old plugin file couldn't be deleted")



            # plugin folder is on sftp or ftp server
            case _:
                plugin_path = f"{plugin_path}/{plugin.plugin_file_name}"
                match (plugin.plugin_repository):
                    case "spigot":
                        try:
                            get_specific_plugin_spiget(plugin.plugin_repository_data[0])
                        except HTTPError as err:
                            rich_print_error(f"HTTPError: {err.code} - {err.reason}")
                            plugins_updated -= 1
                        except TypeError:
                            rich_print_error(
                                f"Error: TypeError > Couldn't download new version. Is the file available on spigotmc?"
                            )
                            plugins_updated -= 1

                    case _:
                        rich_print_error("Error: Plugin repository wasn't found")
                        return None
                # don't delete old plugin files if they are downloaded to a seperate download path
                if config_values.remote_seperate_download_path == False:
                    match config_values.connection:
                        case "sftp":
                            try:
                                connection.remove(plugin_path)
                                rich_console.print(
                                    "    [not bold][bright_green]Deleted old plugin file [cyan]→ [white]" + 
                                    f"{plugin.plugin_file_name}"
                                )
                            except FileNotFoundError:
                                rich_print_error("Error: Old plugin file couldn't be deleted")
                        case "ftp":
                            try:
                                connection.delete(plugin_path)
                                rich_console.print(
                                    "    [not bold][bright_green]Deleted old plugin file [cyan]→ [white]" + 
                                    f"{plugin.plugin_file_name}"
                                )
                            except FileNotFoundError:
                                rich_print_error("Error: Old plugin file couldn't be deleted")

    rich_console.print(
        f"\n[not bold][bright_green]Plugins updated: {plugins_updated}/{(len(INSTALLEDPLUGINLIST) - plugins_skipped)}"
    )
    return None


def search_plugin_spiget(plugin_file: str, plugin_file_name: str, plugin_file_version: str) -> int:
    """
    Search the spiget api for the installed plugin and add it to the installed plugin list

    :param plugin_file: Full file name of plugin
    :param plugin_file_name: Name of plugin file
    :param plugin_file_version: Version of plugin file

    :returns: Plugin ID of Spigot Plugin
    """
    url = f"https://api.spiget.org/v2/search/resources/{plugin_file_name}?field=name&sort=-downloads"
    plugin_list = api_do_request(url)
    
    # Handle failed api request
    """{'error': 'Unexpected Exception', 'msg': 'Unexpected Exception. Please report this to https://github.com/SpiGetOrg/api.spiget.org/issues'}"""
    if "error" in plugin_list:
        print(f"Spiget error occurred whilst searching for plugin '{plugin_file}': {plugin_list['msg']}")
        return plugin_list['msg']
    else:
        plugin_file_version2 = plugin_file_version
        for i in range(4):
            if i == 1:
                plugin_file_version2 = re.sub(r'(\-\w*)', '', plugin_file_version)
            if i == 2:
                plugin_name_in_yml, plugin_version_in_yml = egg_cracking_jar(plugin_file)
                url = f"https://api.spiget.org/v2/search/resources/{plugin_name_in_yml}?field=name&sort=-downloads"
                try:
                    plugin_list = api_do_request(url)
                except ValueError:
                    continue
                # if no plugin name was found with egg_cracking_jar() skip this round
                if plugin_list is None:
                    continue

            # search with version which is in plugin.yml for the plugin
            if i == 3:
                plugin_file_version2 = plugin_version_in_yml


            for plugin in plugin_list:
                plugin_id = plugin["id"]
                url2 = f"https://api.spiget.org/v2/resources/{plugin_id}/versions?size=100&sort=-name"
                try:
                    plugin_versions = api_do_request(url2)
                except ValueError:
                    continue
                if plugin_versions is None:
                    continue
                for updates in plugin_versions:
                    update_version_name = updates["name"]
                    if plugin_file_version2 in update_version_name:
                        #spigot_update_id = updates["id"]
                        plugin_latest_version = get_latest_plugin_version_spiget(plugin_id)
                        plugin_is_outdated = compare_plugin_version(plugin_latest_version, update_version_name)
                        Plugin.add_to_plugin_list(
                            plugin_file,
                            plugin_file_name,
                            plugin_file_version,
                            plugin_latest_version,
                            plugin_is_outdated,
                            "spigot",
                            [plugin_id]
                        )
                        return plugin_id
        return None
