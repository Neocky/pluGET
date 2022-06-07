"""
	Holds all the utilitie code for pluGET and the webrequests function
"""

import os
import sys
import requests
import shutil
from pathlib import Path
from rich.console import Console


def api_do_request(url) -> list:
	"""
		Handles the webrequest and returns a json list
	"""
	webrequest_header = {'user-agent': 'pluGET/1.0'}
	try:
		response = requests.get(url, headers=webrequest_header)
	except:
		print("Couldn't create webrequest")
		return
	api_json_data = response.json()
	return api_json_data


def api_test_spiget() -> None:
	"""
		Test if the Spiget api sends a 200 status code back
	"""
	try:
		r = requests.get('https://api.spiget.org/v2/status')
	except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
		rich_print_error("Error: Couldn't make a connection to the API. Check you connection to the internet!", style="bright_red")
		rich_print_error("Press any key + enter to exit...")
		sys.exit()
	if r.status_code != 200:
		rich_print_error("Error: Problems with the API detected. Plese try it again later!")
		rich_print_error("Press any key + enter to exit...")
		sys.exit()
	return


def rich_print_error(error_message) -> None:
	"""
		Prints a formatted error message from rich
	"""
	console = Console()
	console.print(error_message, style="bright_red")
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
		rich_print_error("Please check for missing permissions in folder tree!")
		input("Press any key + enter to exit...")
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
