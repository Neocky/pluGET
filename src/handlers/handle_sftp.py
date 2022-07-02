import sys
import os
import pysftp
import paramiko
import stat
import re

from src.utils.console_output import rich_print_error
from src.handlers.handle_config import config_value


def sftp_create_connection():
    """
    Creates a sftp connection with the given values in the config file

    :returns: SFTP connection type
    """
    config_values = config_value()
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None # TODO fix this
    try:
        sftp = pysftp.Connection(config_values.server, username=config_values.username, \
               password=config_values.password, port=config_values.sftp_port, cnopts=cnopts)
    except paramiko.ssh_exception.AuthenticationException:
        rich_print_error("Error: [SFTP]: Wrong Username/Password")
    except paramiko.ssh_exception.SSHException:
        rich_print_error("Error: [SFTP]: The SFTP server isn't available.")
    try:
        return sftp
    except UnboundLocalError:
        rich_print_error("Error: [SFTP]: Check your config file!")
        rich_print_error("Exiting program...")
        sys.exit()


def sftp_show_plugins(sftp) -> None:
    """
    Prints all plugins in the sftp folder

    :param sftp: sftp connection

    :returns: None
    """
    config_values = config_value()
    sftp.cd(config_values.remote_plugin_folder_on_server)
    for attr in sftp.listdir_attr():
        print(attr.filename, attr)
    sftp.close()
    return None


def sftp_upload_file(sftp, path_item) -> None:
    """
    Uploads a file to the set folder from the config file

    :param sftp: sftp connection
    :param path_item: The upload path with the item name

    :returns: None
    """
    config_values = config_value()
    if config_values.remote_seperate_download_path is True:
        path_upload_folder = config_values.remote_path_to_seperate_download_path
    else:
        path_upload_folder = config_values.remote_plugin_folder_on_server
    try:
        sftp.chdir(path_upload_folder)
        sftp.put(path_item)
    except FileNotFoundError:
        rich_print_error("Error: [SFTP]: The 'plugins' folder couldn't be found on the remote host!")
        rich_print_error("Error: [SFTP]: Aborting uploading.")
    sftp.close()
    return None


def sftp_upload_server_jar(sftp, path_item) -> None:
    """
    Uploads the server jar to the root folder

    :param sftp: sftp connection
    :param path_item: The upload path with the item name

    :returns: None
    """
    try:
        sftp.chdir('.')
        sftp.put(path_item)
    except FileNotFoundError:
        rich_print_error("Error: [SFTP]: The 'root' folder couldn't be found on the remote host!")
        rich_print_error("Error: [SFTP]: Aborting uploading.")
    sftp.close()
    return None


def sftp_list_all(sftp):
    """
    List all plugins in the 'plugins' folder on the sftp host

    :param sftp: sftp connection

    :return: List of plugins in plugin folder
    """
    config_values = config_value()
    try:
        sftp.chdir(config_values.remote_plugin_folder_on_server)
        installed_plugins = sftp.listdir()
    except FileNotFoundError:
        rich_print_error("Error: [SFTP]: The 'plugins' folder couldn't be found on the remote host!")

    try:
        return installed_plugins
    except UnboundLocalError:
        rich_print_error("Error: [SFTP]: No plugins were found.")


def sftp_list_files_in_server_root(sftp):
    """
    List all files in the root folder on the sftp host

    :param sftp: sftp connection

    :returns: List of files in root folder
    """
    try:
        files_in_server_root = sftp.listdir()
    except FileNotFoundError:
        rich_print_error("Error: [SFTP]: The 'root' folder couldn't be found on the remote host!")
    try:
        return files_in_server_root
    except UnboundLocalError:
        rich_print_error("Error: [SFTP]: No Serverjar was found.")


def sftp_download_file(sftp, file) -> None:
    """
    Downloads a plugin file from the sftp host to a temporary folder

    :param sftp: sftp connection
    :param file: Filename of plugin

    :returns: None
    """
    config_values = config_value()
    sftp.cwd(config_values.remote_plugin_folder_on_server)
    current_directory = os.getcwd()
    os.chdir('TempSFTPFolder')
    sftp.get(file)
    sftp.close()
    os.chdir(current_directory)
    return None


def sftp_validate_file_attributes(sftp, plugin_path) -> bool:
    """
    Check if the file is a legitimate plugin file

    :param sftp: sftp connection
    param plugin_path: Path of the single plugin file

    :returns: If file is a plugin file or not 
    """
    plugin_sftp_attribute = sftp.lstat(plugin_path)
    if stat.S_ISDIR(plugin_sftp_attribute.st_mode):
        return False
    elif re.search(r'.jar$', plugin_path):
        return True
    else:
        return False
