"""
File and functions which handle the download of the specific plugins
"""

import re
import urllib.request
from urllib.error import HTTPError
from pathlib import Path

import rich

from src.utils.utilities import convert_file_size_down, remove_temp_plugin_folder, create_temp_plugin_folder
from src.utils.utilities import api_do_request
from src.utils.console_output import rich_print_error
from src.handlers.handle_config import config_value


def handle_regex_package_name(full_plugin_name) -> str:
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


def get_version_id(plugin_id, plugin_version) -> str:
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
	if response == None:
		return None
	for plugins in version_list:
		plugin_update = plugins["name"]
		version_id = plugins["id"]
	if plugin_update == plugin_version:
		return version_id
	return version_list[0]["id"]


def get_version_name(plugin_id, plugin_version_id) -> str:
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


def download_specific_plugin_version(plugin_id, download_path, version_id="latest") -> None:
	"""
	Download a specific plugin
	"""
	#config_values = config_value()
	if version_id != "latest" and version_id != None:
		#url = f"https://spigotmc.org/resources/{plugin_id}/download?version={versionID}"
		rich_print_error("Sorry but specific version downloads aren't supported because of cloudflare protection. :(")
		rich_print_error("Reverting to latest version.")

	#url = f"https://api.spiget.org/v2/resources/{plugin_id}/versions/latest/download" #throws 403 forbidden error...cloudflare :(
	url = f"https://api.spiget.org/v2/resources/{plugin_id}/download"

	urrlib_opener = urllib.request.build_opener()
	urrlib_opener.addheaders = [('User-agent', 'pluGET/1.0')]
	urllib.request.install_opener(urrlib_opener)

	remote_file = urllib.request.urlopen(url)
	try:
		file_size = int(remote_file.info()['Content-Length'])
	except TypeError:
		# if api won't return file size set it to 0 to avoid throwing an error
		file_size = 0
	urllib.request.urlretrieve(url, download_path)
	print("		", end='')
	if file_size >= 1000000 and file_size != 0:
		file_size_data = convert_file_size_down(convert_file_size_down(file_size))
		print("Downloaded " + (str(file_size_data)).rjust(9) + f" MB here {download_path}")
	elif file_size != 0:
		file_size_data = convert_file_size_down(file_size)
		print("Downloaded " + (str(file_size_data)).rjust(9) + f" KB here {download_path}")
	else:
		print(f"Downloaded         file here {download_path}")
	# TODO add sftp and ftp support
	#if config_values.connection == "sftp":
	#	sftp_session = createSFTPConnection()
	#	sftp_upload_file(sftp_session, download_path)
	#elif config_values.connection == "ftp":
	#	ftp_session = createFTPConnection()
	#	ftp_upload_file(ftp_session, download_path)
	return None


def get_specific_plugin(plugin_id, plugin_version="latest") -> None:
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
		# exit if plugin id coudn't be found
		rich_print_error("Error: Plugin ID couldn't be found")
		return None
	plugin_name = handle_regex_package_name(plugin_name)
	plugin_version_id = get_version_id(plugin_id, plugin_version)
	plugin_version_name = get_version_name(plugin_id, plugin_version_id)
	plugin_download_name = f"{plugin_name}-{plugin_version_name}.jar"
	download_plugin_path = Path(f"{download_path}/{plugin_download_name}")
	# set the plugin_version_id to None if a specific version wasn't given as parameter
	if plugin_version == "latest" or plugin_version is None:
		plugin_version_id = None
	download_specific_plugin_version(plugin_id, download_plugin_path, plugin_version_id)

	if config_values.connection != "local":
		remove_temp_plugin_folder()
	return None
