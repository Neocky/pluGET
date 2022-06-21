import os
import sys
import ftplib
import re

from src.utils.console_output import rich_print_error
from src.handlers.handle_config import config_value


def ftp_create_connection():
    """
    Creates a connection to the ftp server with the given values in the config

    :returns: ftp connection type
    """
    config_values = config_value()
    try:
        ftp = ftplib.FTP()
        ftp.connect(config_values.server, config_values.ftp_port)
        ftp.login(config_values.username, config_values.password)
        return ftp
    except UnboundLocalError:
        rich_print_error("Error: [SFTP]: Check your config file!")
        rich_print_error("Exiting program...")
        sys.exit()


def ftp_show_plugins(ftp) -> None:
    """
    Prints all plugins in the plugin folder
    
    :param ftp: ftp connection

    :returns: None
    """
    config_values = config_value()
    ftp.cwd(config_values.remote_plugin_folder_on_server)
    for attr in ftp.dir():
        print(attr.filename, attr)
    return None


def ftp_upload_file(ftp, path_item) -> None:
    """
    Uploads a file to the ftp server

    :param ftp: ftp connection
    :param path_item: Name of the item which should be uploaded

    :returns: None
    """
    config_values = config_value()
    if config_values.remote_seperate_download_path is True:
        path_upload_folder = config_values.remote_path_to_seperate_download_path
    else:
        path_upload_folder = config_values.remote_plugin_folder_on_server
    try:
        ftp.cwd(path_upload_folder)
        path_item = os.path.relpath(path_item, 'TempSFTPFolder/')
        path_item = str(path_item)
        current_directory = os.getcwd()
        os.chdir('TempSFTPFolder')
        with open (path_item, 'rb') as plugin_file:
            ftp.storbinary('STOR '+ str(path_item), plugin_file)
    except FileNotFoundError:
        rich_print_error("Error: [FTP]: The 'plugins' folder couldn't be found on the remote host!")
        rich_print_error("Error: [FTP]: Aborting uploading.")
    os.chdir(current_directory)
    ftp.close()
    return None


def ftp_upload_server_jar(ftp, path_item) -> None:
    """
    Uploads a serverjar to the root folder of the ftp host

    :param ftp: ftp connection
    :param path_item: Name of the file which should be uploaded

    :returns: None
    """
    try:
        ftp.cwd('.')
        path_item = os.path.relpath(path_item, 'TempSFTPFolder/')
        path_item = str(path_item)
        current_directory = os.getcwd()
        os.chdir('TempSFTPFolder')
        with open (path_item, 'rb') as server_jar:
            ftp.storbinary('STOR '+ str(path_item), server_jar)
    except FileNotFoundError:
        rich_print_error("Error: [FTP]: The 'root' folder couldn't be found on the remote host!")
        rich_print_error("Error: [FTP]: Aborting uploading.")
    os.chdir(current_directory)
    ftp.close()
    return None


def ftp_list_all(ftp):
    """
    Returns a list with all installed plugins in the plugin folder of the ftp host

    :param ftp: ftp connection

    :returns: List of all plugins in plugin folder
    """
    config_values = config_value()
    try:
        ftp.cwd(config_values.remote_plugin_folder_on_server)
        installed_plugins = ftp.nlst()
    except FileNotFoundError:
        rich_print_error("Error: [FTP]: The 'plugins' folder couldn't be found on the remote host!")

    try:
        return installed_plugins
    except UnboundLocalError:
        rich_print_error("Error: [FTP]: No plugins were found.")


def ftp_listFilesInServerRoot(ftp):
    """
    Returns a list with all files in the root folder of the ftp host

    :param ftp: ftp connection

    :returns: List of all files in root folder
    """
    try:
        ftp.cwd('.')
        filesInServerRoot = ftp.nlst()
    except FileNotFoundError:
        rich_print_error("Error: [FTP]: The 'root' folder couldn't be found on the remote host!")

    try:
        return filesInServerRoot
    except UnboundLocalError:
        rich_print_error("Error: [FTP]: No Serverjar was found.")


def ftp_downloadFile(ftp, path_download, file) -> None:
    """
    Download a file of the ftp server

    :param ftp: ftp connection
    :param path_download: Path to save downloaded file to
    :param file: File to download

    :returns None
    """
    config_values = config_value()
    ftp.cwd(config_values.remote_plugin_folder_on_server)
    filedata = open(path_download,'wb')
    ftp.retrbinary('RETR '+file, filedata.write)
    filedata.close()
    ftp.quit()
    return None


def ftp_is_file(ftp, plugin_path) -> bool:
    """
    Check if file on ftp host is a file and not a directory

    :param ftp: ftp connection
    :param plugin_path

    :returns: True if file is a file and not a directory
    """
    if ftp.nlst(plugin_path) == [plugin_path]:
        return True
    else:
        return False


def ftp_validate_file_attributes(ftp, plugin_path) -> bool:
    """
    Check if a file is a legitimate plugin file

    :param ftp: ftp connection
    :param plugin_path: Path of file to check
    
    :returns: If file is a plugin file or not
    """
    if ftp_is_file(ftp, plugin_path) is False:
        return False
    if re.search(r'.jar$', plugin_path):
        return True
    else:
        return False
