"""Handles the logic for the config validation, reading, and creating.

This module defines the configuration structure and utilities to manage
the 'pluGET_config.yaml' file.
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union, Optional

import ruamel.yaml
from rich.console import Console


class ConfigValue:
    """Holds all the available configuration values from the config file.
    
    Attributes:
        connection (str): Type of connection ('local', 'sftp', 'ftp').
        path_to_plugin_folder (Path): Local path to plugins.
        local_seperate_download_path (bool): Whether to use a separate download path locally.
        local_path_to_seperate_download_path (Path): The separate local download path.
        server (str): Remote server address.
        username (str): Remote username.
        password (str): Remote password.
        sftp_port (int): Port for SFTP.
        ftp_port (int): Port for FTP.
        remote_seperate_download_path (bool): Whether to use a separate download path remotely.
        remote_path_to_seperate_download_path (str): The separate remote download path.
        remote_plugin_folder_on_server (str): Path to plugins on the remote server.
    """

    def __init__(self) -> None:
        """Initializes ConfigValue by loading data from the YAML file."""
        yaml = ruamel.yaml.YAML()
        config_path = Path("pluGET_config.yaml")
        
        if not config_path.exists():
            # Fallback or error handling if file doesn't exist when class is instantiated
            # Ideally check_config() ensures existence before this class is called.
            pass

        try:
            with config_path.open("r", encoding="utf-8") as config_file:
                data: Dict[str, Any] = yaml.load(config_file)
        except (OSError, ruamel.yaml.YAMLError) as e:
            print(f"Critical Error: Could not read config file: {e}")
            sys.exit(1)

        self.connection: str = str(data["Connection"]).lower()
        self.path_to_plugin_folder: Path = Path(data["Local"]["PathToPluginFolder"])
        self.local_seperate_download_path: bool = bool(
            data["Local"]["SeperateDownloadPath"]
        )
        self.local_path_to_seperate_download_path: Path = Path(
            data["Local"]["PathToSeperateDownloadPath"]
        )
        self.server: str = str(data["Remote"]["Server"])
        self.username: str = str(data["Remote"]["Username"])
        self.password: str = str(data["Remote"]["Password"])
        self.sftp_port: int = int(data["Remote"]["SFTP_Port"])
        self.ftp_port: int = int(data["Remote"]["FTP_Port"])
        self.remote_seperate_download_path: bool = bool(
            data["Remote"]["SeperateDownloadPath"]
        )
        # Remote paths remain strings as Path() is OS-dependent (local Windows vs remote Linux)
        self.remote_path_to_seperate_download_path: str = str(
            data["Remote"]["PathToSeperateDownloadPath"]
        )
        self.remote_plugin_folder_on_server: str = str(
            data["Remote"]["PluginFolderOnServer"]
        )


# Backward compatibility alias if other files import 'config_value'
config_value = ConfigValue


def check_config() -> None:
    """Checks if the config file exists.

    If 'pluGET_config.yaml' does not exist in the current directory,
    it creates a new default configuration and exits the program.
    """
    if not os.path.isfile("pluGET_config.yaml"):
        create_config()
    return None


def create_config() -> None:
    """Creates the YAML config file with default values and exits the program.
    
    This function writes the default 'pluGET_config.yaml' to the disk
    and prompts the user to edit it before restarting.
    """
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
    yaml = ruamel.yaml.YAML()
    code = yaml.load(configuration)
    
    try:
        with open("pluGET_config.yaml", "w", encoding="utf-8") as config_file:
            yaml.dump(code, config_file)
    except OSError as e:
        print(f"Error creating config file: {e}")
        sys.exit(1)

    config_file_path = os.path.abspath("pluGET_config.yaml")
    print(f"Path of config file: {config_file_path}")
    print("Config created. Edit config before executing again!")
    input("Press any key + enter to exit...")
    sys.exit()


def validate_config() -> None:
    """Validates critical configuration variables.

    Checks if the 'Connection' setting in the config is valid.
    Exits the program if invalid settings are found.
    """
    accepted_values: Tuple[str, ...] = ("local", "sftp", "ftp")
    exit_afterwards = False
    
    # Load config logic
    try:
        config = ConfigValue()
    except Exception:
        # ConfigValue handles its own exit on failure usually
        return

    console = Console()
    
    if config.connection not in accepted_values:
        console.print(
            f"Error in Config! Accepted values for key 'Connection' are {accepted_values}",
            style="bright_red",
        )
        exit_afterwards = True
        
    if exit_afterwards:
        sys.exit()
