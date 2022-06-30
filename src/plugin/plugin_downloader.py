"""
File and functions which handle the download of the specific plugins
"""

import re
from pathlib import Path
import requests

from rich.table import Table
from rich.console import Console
from rich.progress import Progress

from src.utils.utilities import convert_file_size_down, remove_temp_plugin_folder, create_temp_plugin_folder
from src.utils.utilities import api_do_request
from src.utils.console_output import rich_print_error
from src.handlers.handle_config import config_value
from src.handlers.handle_sftp import sftp_create_connection, sftp_upload_file
from src.handlers.handle_ftp import ftp_create_connection, ftp_upload_file


def handle_regex_plugin_name(full_plugin_name) -> str:
    """
    Return the plugin name after trimming clutter from name with regex operations
    """
    # trims the part of the package that has for example "[1.1 Off]" in it
    unwanted_plugin_name = re.search(r'(^\[+[a-zA-Z0-9\s\W*\.*\-*\+*\%*\,]*\]+)', full_plugin_name)
    if bool(unwanted_plugin_name):
        unwanted_plugin_name_string = unwanted_plugin_name.group()
        full_plugin_name = full_plugin_name.replace(unwanted_plugin_name_string, '')

    # gets the real plugin_name "word1 & word2" is not supported only gets word1
    plugin_name = re.search(r'([a-zA-Z]\d*)+(\s?\-*\_*[a-zA-Z]\d*\+*\-*\'*)+', full_plugin_name)
    try:
        plugin_name_full_string = plugin_name.group()
        found_plugin_name = plugin_name_full_string.replace(' ', '')
    except AttributeError:
        found_plugin_name = unwanted_plugin_name_string
    return found_plugin_name


def get_version_id_spiget(plugin_id, plugin_version) -> str:
    """
    Returns the version id of the plugin
    """
    if plugin_version == None or plugin_version == 'latest':
        url = f"https://api.spiget.org/v2/resources/{plugin_id}/versions/latest"
        response = api_do_request(url)
        if response == None:
            return None
        version_id = response["id"]
        return version_id

    url = f"https://api.spiget.org/v2/resources/{plugin_id}/versions?size=100&sort=-name"
    version_list = api_do_request(url)
    if version_list == None:
        return None
    for plugins in version_list:
        plugin_update = plugins["name"]
        version_id = plugins["id"]
        if plugin_update == plugin_version:
            return version_id
    return version_list[0]["id"]


def get_version_name_spiget(plugin_id, plugin_version_id) -> str:
    """
    Returns the name of a specific version
    """
    url = f"https://api.spiget.org/v2/resources/{plugin_id}/versions/{plugin_version_id}"
    response = api_do_request(url)
    if response == None:
        return None
    version_name = response["name"]
    return version_name


def get_download_path(config_values) -> str:
    """
    Reads the config and gets the path of the plugin folder
    """
    match (config_values.connection):
        case "local":
            match (config_values.local_seperate_download_path):
                case True:
                    return config_values.local_path_to_seperate_download_path
                case _:
                    return config_values.path_to_plugin_folder
        case _:
            match (config_values.remote_seperate_download_path):
                case True:
                    return config_values.remote_path_to_seperate_download_path
                case _:
                    return config_values.remote_plugin_folder_on_server


def download_specific_plugin_version_spiget(plugin_id, download_path, version_id="latest") -> None:
    """
    Download a specific plugin
    """
    config_values = config_value()
    if version_id != "latest" and version_id != None:
        #url = f"https://spigotmc.org/resources/{plugin_id}/download?version={versionID}"
        rich_print_error("Sorry but specific version downloads aren't supported because of cloudflare protection. :(")
        rich_print_error("Reverting to latest version.")

    #throws 403 forbidden error...cloudflare :(
    #url = f"https://api.spiget.org/v2/resources/{plugin_id}/versions/latest/download"

    url = f"https://api.spiget.org/v2/resources/{plugin_id}/download"

    # use rich Progress() to create progress bar
    with Progress(transient=True) as progress:
        header = {'user-agent': 'pluGET/1.0'}
        r = requests.get(url, headers=header, stream=True)
        try:
            file_size = int(r.headers.get('content-length'))
            # create progress bar
            download_task = progress.add_task("    [cyan]Downloading...", total=file_size)
        except TypeError:
            # Content-lenght returned nothing
            file_size = 0
        with open(download_path, 'wb') as f:
            # split downloaded data in chunks of 32768
            for data in r.iter_content(chunk_size=32768):
                f.write(data)
                # don't show progress bar if no content-length was returned
                if file_size == 0:
                    continue
                progress.update(download_task, advance=len(data))
                #f.flush()

    # use rich console for nice colors
    console = Console()
    if file_size == 0:
        console.print(
            f"    [not bold][bright_green]Downloaded[bright_magenta]         file [cyan]→ [white]{download_path}"
        )
    elif file_size >= 1000000:
        file_size_data = convert_file_size_down(convert_file_size_down(file_size))
        console.print("    [not bold][bright_green]Downloaded[bright_magenta] " + (str(file_size_data)).rjust(9) + \
             f" MB [cyan]→ [white]{download_path}")
    else:
        file_size_data = convert_file_size_down(file_size)
        console.print("    [not bold][bright_green]Downloaded[bright_magenta] " + (str(file_size_data)).rjust(9) + \
             f" KB [cyan]→ [white]{download_path}")

    if config_values.connection == "sftp":
        sftp_session = sftp_create_connection()
        sftp_upload_file(sftp_session, download_path)
    elif config_values.connection == "ftp":
        ftp_session = ftp_create_connection()
        ftp_upload_file(ftp_session, download_path)
    return None


def get_specific_plugin_spiget(plugin_id, plugin_version="latest") -> None:
    """
    Gets the specific plugin and calls the download function
    """
    config_values = config_value()
    # use a temporary folder to store plugins until they are uploaded
    if config_values.connection != "local":
        download_path = create_temp_plugin_folder()
    else:
        download_path = get_download_path(config_values)

    url = f"https://api.spiget.org/v2/resources/{plugin_id}"
    plugin_details = api_do_request(url)
    if plugin_details == None:
        return None
    try:
        plugin_name = plugin_details["name"]
    except KeyError:
        # exit if plugin id couldn't be found
        rich_print_error("Error: Plugin ID couldn't be found")
        return None
    plugin_name = handle_regex_plugin_name(plugin_name)
    plugin_version_id = get_version_id_spiget(plugin_id, plugin_version)
    plugin_version_name = get_version_name_spiget(plugin_id, plugin_version_id)
    plugin_download_name = f"{plugin_name}-{plugin_version_name}.jar"
    download_plugin_path = Path(f"{download_path}/{plugin_download_name}")
    # if api requests weren't successfull stop function
    if plugin_version_id == None or plugin_version_name == None:
        rich_print_error("Error: Webrequest timed out")
        return None
    # set the plugin_version_id to None if a specific version wasn't given as parameter
    if plugin_version == "latest" or plugin_version is None:
        plugin_version_id = None
    download_specific_plugin_version_spiget(plugin_id, download_plugin_path, plugin_version_id)

    if config_values.connection != "local":
        remove_temp_plugin_folder()
    return None


def search_specific_plugin_spiget(plugin_name) -> None:
    """
    Search for a name and return the top 10 results sorted for their download count
    Then ask for input and download that plugin
    """
    url= f"https://api.spiget.org/v2/search/resources/{plugin_name}?field=name&sort=-downloads"
    plugin_search_results = api_do_request(url)
    if plugin_search_results == None:
        rich_print_error("Error: Webrequest wasn't successfull!")
        return None

    print(f"Searching for {plugin_name}...")
    print(f"Found plugins:")
    # create table with rich
    rich_table = Table(box=None)
    rich_table.add_column("No.", justify="right", style="cyan", no_wrap=True)
    rich_table.add_column("Name", style="bright_magenta")
    rich_table.add_column("Downloads", justify="right", style="bright_green")
    rich_table.add_column("Description", justify="left", style="white")
    # start counting at 1 for all my non-programming friends :)
    i = 1
    for found_plugin in plugin_search_results:
        plugin_name = handle_regex_plugin_name(found_plugin["name"])
        plugin_downloads = found_plugin["downloads"]
        plugin_description = found_plugin["tag"]
        rich_table.add_row(str(i), plugin_name, str(plugin_downloads), plugin_description)
        i += 1

    # print table from rich
    rich_console = Console()
    rich_console.print(rich_table)

    try:
        plugin_selected = input("Select your wanted resource (No.)(0 to exit): ")
    except KeyboardInterrupt:
        return None
    if plugin_selected == "0":
        return None
    try:
        plugin_selected =  int(plugin_selected) - 1
        plugin_selected_id = plugin_search_results[plugin_selected]["id"]
    except ValueError:
        rich_print_error("Error: Input wasn't a number! Please try again!")
        return None
    except IndexError:
        rich_print_error("Error: Number was out of range! Please try again!")
        return None
    selected_plugin_name = handle_regex_plugin_name(plugin_search_results[plugin_selected]["name"])
    rich_console.print(f"\n [not bold][bright_white]● [bright_magenta]{selected_plugin_name} [bright_green]latest")
    get_specific_plugin_spiget(plugin_selected_id)
