""""
	Handles the logic for the config validation, reading and creating
"""

import os
import sys
import ruamel.yaml
import shutil
from pathlib import Path
from rich.console import Console
from src.servers.local import local_server
from src.servers.ftp import ftp_server
from src.servers.sftp import sftp_server
from src.handlers.handle_server import server_list
from src.handlers import handle_server

def read_config():
	"""
	Reads the config file and populates the server handler
	"""
	yaml = ruamel.yaml.YAML()
	with open("config.yaml", "r") as config_file:
		data = yaml.load(config_file)
	for server in data["Servers"]:
		data2 = data["Servers"][server]
		
		match data2["Connection"]:
			case "local":
				temp = local_server()
			case "ftp":
				temp = ftp_server()
			case "sftp":
				temp = sftp_server()

		temp.name = str(server)
		temp.connection = data2["Connection"]
		temp.root_path = Path(data2["ServerRootPath"])
		temp.plugin_path = Path(data2["PluginFolderPath"])
		temp.seperate_download_path = data2["SeperateDownloadPath"]
		if temp.connection == "sftp" or temp.connection == "ftp":
			temp.server = data2["Server"]
			temp.username = data2["Username"]
			temp.password = data2["Password"]
			temp.port = int(data2["Port"])

		server_list[str(server)] = temp
	handle_server.active_server = server_list[next(iter(server_list))]
	

def check_config() -> None:
	"""
	Check if there is a pluGET_config.yml file in the same folder as pluget.py and if not create a new config
	and exit the programm
	"""
	if not os.path.isfile("config.yaml"):
		create_config()
	return None


def create_config() -> None:
	"""
	copies the sample config file into the root folder
	"""
	shutil.copyfile('src/config-sample.yaml', 'config.yaml')
	config_file_path = os.path.abspath("config.yaml")
	print(f"Path of config file: {config_file_path}")
	print("Config created. Edit config before executing again!")
	input("Press any key + enter to exit...")
	sys.exit()

def validate_config() -> None:
	"""
	Check for missing entries in the config
	"""
	yaml = ruamel.yaml.YAML()
	with open("config.yaml", "r") as config_file:
		data = yaml.load(config_file)
	console = Console()
	exit_afterwards = False

	if "Servers" not in data:
		console.print(f"Config file is malformed",style="bright_red",highlight=False)
		exit_afterwards = True
	else:
		for server in data["Servers"]:
			temp = data["Servers"][server]
			keys = ["Connection","ServerRootPath","PluginFolderPath","SeperateDownloadPath"]
			remote_keys = ["Server","Username","Password","port"]
			
			if temp == None:
				console.print(f"'{str(server)}' is malformed",style="bright_red",highlight=False)
				exit_afterwards = True
			else:
				for cur in keys:
					if cur not in temp:
						console.print(f"'{str(server)}' is missing key '{cur}'",style="bright_red",highlight=False)
						exit_afterwards = True

				if "Connection" in temp:
					accepted_values = ("local", "sftp", "ftp")
					if temp["Connection"] not in accepted_values:
						console.print(f"'{server}' has invalid key 'Connection' Valid options: {accepted_values}",style="bright_red",highlight=False)
						exit_afterwards = True

					if temp["Connection"] == "sftp" or temp["Connection"] == "ftp":
						for cur in remote_keys:
							if cur not in temp:
								console.print(f"'{str(server)}' is missing key '{cur}'",style="bright_red",highlight=False)
								exit_afterwards = True
	if exit_afterwards: 
		sys.exit()
		

