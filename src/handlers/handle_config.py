""""
	Handles the logic for the config validation, reading and creating
"""

import os
import sys
import ruamel.yaml
from pathlib import Path
from rich.console import Console


class config_value():
	"""
		Class which holds all the available configuration values from the config file and which will be used later in
		the process of updating plugins
		If bool in config can't be read it will default to 'False'
	"""
	def __init__(self):
		yaml = ruamel.yaml.YAML()
		with open("pluget_config.yaml", "r") as config_file:
			data = yaml.load(config_file)
		self.connection = data["Connection"]
		self.path_to_plugin_folder = Path(data["Local"]["PathToPluginFolder"])
		self.local_seperate_download_path = True if data["Local"]["SeperateDownloadPath"] == True else False
		self.local_path_to_seperate_download_path = Path(data["Local"]["PathToSeperateDownloadPath"])
		self.server = data["Remote"]["Server"]
		self.username = data["Remote"]["Server"]
		self.password = data["Remote"]["Password"]
		self.sftp_port = int(data["Remote"]["SFTP_Port"])
		self.ftp_port = int(data["Remote"]["FTP_Port"])
		self.remote_seperate_download_path = True if data["Remote"]["SeperateDownloadPath"] == True else False
		self.remote_path_to_seperate_download_path = data["Remote"]["PathToSeperateDownloadPath"]
		self.remote_plugin_folder_on_server = data["Remote"]["PluginFolderOnServer"]


def check_config() -> None:
	"""
		Check if there is a pluget_config.yml file in the same folder as pluget.py and if not create a new config
		and exit the programm
	"""
	if not os.path.isfile("pluget_config.yaml"):
		create_config()


def create_config() -> None:
	"""
		Creates the yaml config in the current directory with the filename pluget_config.yml
	"""
	# this is the whole yaml code because of weird formating indention is not possible 
	configuration = """\
#
# Configuration File for pluGET
# https://www.github.com/Neocky/pluGET 
#

# What should be used for the connection (local, sftp, ftp)
    Connection: local

    Local:
        PathToPluginFolder: C:/Users/USER/Desktop/plugins
  # If a different folder should be used to store the updated plugins change to (True/False) and the path below
        SeperateDownloadPath : False
        PathToSeperateDownloadPath: C:/Users/USER/Desktop/plugins

    Remote:
        Server: 0.0.0.0
        Username: user
        Password: password
  # If a different Port for SFTP/FTP will be used
        SFTP_Port: 22
        FTP_Port: 21
  # If a different folder should be used to store the updated plugins change to (True/False) and the path below
        SeperateDownloadPath : False
        PathToSeperateDownloadPath: /plugins/updated
  # Change the path below if the plugin folder path is different on the SFTP/FTP server (Change only if you know what you are doing)
        PluginFolderOnServer: /plugins
    """
	# load ruamel.yaml to get the # commands right in the yaml code
	yaml = ruamel.yaml.YAML()
	code = yaml.load(configuration)
	print(code['Local']['SeperateDownloadPath'])
	with open("pluget_config.yaml", "w") as config_file:
		yaml.dump(code, config_file)

	config_file_path = os.path.abspath("pluget_config.yaml")
	print(f"Path of config file: {config_file_path}")
	print("Config created. Edit config before executing again!")
	input("Press any key + enter to exit...")
	sys.exit()


def validate_config() -> None:
	"""
		Validates the config variables after config class is loaded and exit if error is detected and print error
	"""
	accepted_values = [
		("local", "sftp", "ftp")
	]
	# exit afterwards if there is an error in config
	exit_afterwards = False
	config = config_value()
	# rich console for nice colors
	console = Console()
	if (config.connection).lower() not in accepted_values[0]:
		console.print(f"Error in Config! Accepted values for key 'Connection' are {accepted_values[0]}",
		style="bright_red")
		exit_afterwards = True
	if exit_afterwards:
		sys.exit()
