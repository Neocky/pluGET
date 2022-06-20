"""
Holds all the utilitie code for pluGET and the webrequests function
"""

import os
import sys
import requests
import shutil
import re
from pathlib import Path
from rich.console import Console

from src.utils.console_output import rich_print_error
from src.handlers.handle_config import config_value
from src.settings import PLUGETVERSION


def check_for_pluGET_update() -> None:
    """
    Check with the github api if there is a new version for pluGET available and print download message if this is
    the case
    """
    response = api_do_request("https://api.github.com/repos/Neocky/pluGET/releases/latest")
    # get '.1.6.10' as output
    full_version_string = re.search(r"[\.?\d]*$", response["name"])
    # remove '.' to get '1.6.10' as output
    version = re.sub(r"^\.*", "", full_version_string.group())
    console = Console()
    try:
        pluget_installed_version_tuple = tuple(map(int, (PLUGETVERSION.split("."))))
        plugin_latest_version_tuple = tuple(map(int, (version.split("."))))
    except ValueError:
        console.print("Couldn't check if new version of pluGET is available")
        return None
    if pluget_installed_version_tuple < plugin_latest_version_tuple:
        print(f"A new version for pluGET is available: {version}")
        console.print("Download it here: ", end='')
        console.print("https://github.com/Neocky/pluGET", style="link https://github.com/Neocky/pluGET")
    return None


def api_do_request(url) -> list:
    """
    Handles the webrequest and returns a json list
    """
    webrequest_header = {'user-agent': 'pluGET/1.0'}
    try:
        response = requests.get(url, headers=webrequest_header)
    except:
        rich_print_error("Error: Couldn't create webrequest")
        # return None to make functions quit
        return None
    api_json_data = response.json()
    return api_json_data


def api_test_spiget() -> None:
    """
    Test if the Spiget api sends a 200 status code back
    """
    try:
        r = requests.get('https://api.spiget.org/v2/status')
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
        rich_print_error("Error: Couldn't make a connection to the API. Check you connection to the internet!")
        sys.exit()
    if r.status_code != 200:
        rich_print_error("Error: Problems with the API detected. Plese try it again later!")
        sys.exit()
    return None


def create_temp_plugin_folder() -> Path:
    """
    Creates a temporary folder to store plugins inside
    Returns full path of temporary folder
    """
    path_temp_plugin_folder = Path("./TempSFTPFolder")
    if os.path.isdir(path_temp_plugin_folder):
        return path_temp_plugin_folder

    try:
        os.mkdir(path_temp_plugin_folder)
    except OSError:
        rich_print_error(f"Error: Creation of directory {path_temp_plugin_folder} failed")
        rich_print_error("       Please check for missing permissions in folder tree!")
        sys.exit()
    return path_temp_plugin_folder


def remove_temp_plugin_folder() -> None:
    """
    Removes the temporary plugin folder and all content inside it
    """
    try:
        shutil.rmtree(Path("./TempSFTPFolder"))
    except OSError as e:
        rich_print_error(f"Error: {e.filename} - {e.strerror}")
    return


def convert_file_size_down(file_size) -> float:
    """
    Convert the size of the number one down. E.g. MB -> KB through division with 1024
    """
    converted_file_size = (int(file_size)) / 1024
    converted_file_size = round(converted_file_size, 2)
    return converted_file_size


def check_local_plugin_folder(config_values) -> None:
    """
    Check if a local plugin folder exists and if not exit the programm
    """
    if config_values.local_seperate_download_path:
        plugin_folder_path = config_values.local_path_to_seperate_download_path
    else:
        plugin_folder_path = config_values.path_to_plugin_folder
    if not os.path.isdir(plugin_folder_path):
        rich_print_error(f"Error: Local plugin folder '{plugin_folder_path}' couldn't be found! \
        \n       Check the config and try again!")
        sys.exit()
    return None


def check_requirements() -> None:
    """
    Check if the plugin folders are available
    """
    config_values = config_value()
    match config_values.connection:
        case "local":
            check_local_plugin_folder(config_values)
        case "sftp":
            print("Check sftp folder")
        case "ftp":
            print("check ftp folder")
    return None
