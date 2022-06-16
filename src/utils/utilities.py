"""
Holds all the utilitie code for pluGET and the webrequests function
"""

import os
import sys
import requests
import shutil
from pathlib import Path

from src.utils.console_output import rich_print_error
from src.handlers.handle_config import config_value


def api_do_request(url) -> list:
    """
    Handles the webrequest and returns a json list
    """
    webrequest_header = {'user-agent': 'pluGET/1.0'}
    try:
        response = requests.get(url, headers=webrequest_header)
    except:
        print("Couldn't create webrequest")
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
    return


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
