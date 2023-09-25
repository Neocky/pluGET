import sys
import os
import pysftp
import paramiko
import stat
import re

from pathlib import Path
from src.utils.console_output import rich_print_error

class sftp_server():
    def create_connection(self):
        """
        Creates a sftp connection with the given values in the config file
        """
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None # TODO fix this
        try:
            sftp = pysftp.Connection(self.server, username=self.username, \
                password=self.password, port=self.port, cnopts=cnopts)
        except paramiko.ssh_exception.AuthenticationException:
            rich_print_error("Error: [SFTP]: Wrong Username/Password")
        except paramiko.ssh_exception.SSHException:
            rich_print_error("Error: [SFTP]: The SFTP server isn't available.")
        try:
            self.sftp = sftp
        except UnboundLocalError:
            rich_print_error("Error: [SFTP]: Check your config file!")
            rich_print_error("Exiting program...")
            sys.exit()

    def close_connection(self):
        """
        Closes the sftp connection
        """
        self.sftp.close()

    def upload_plugin(self, path_item) -> None:
        """
        Uploads a file to the set folder from the config file

        :param path_item: The upload path with the item name

        :returns: None
        """
        if self.seperate_download_path is not False:
            path_upload_folder = self.seperate_download_path
        else:
            path_upload_folder = self.plugin_path
        try:
            print(path_upload_folder)
            self.sftp.chdir(str(path_upload_folder))
            self.sftp.put(path_item)
        except FileNotFoundError:
            rich_print_error("Error: [SFTP]: The 'plugins' folder couldn't be found on the remote host!")
            rich_print_error("Error: [SFTP]: Aborting uploading.")
        return None

    def upload_server_jar(self, path_item) -> None:
        """
        Uploads the server jar to the root folder

        :param path_item: The upload path with the item name

        :returns: None
        """
        try:
            self.sftp.chdir(self.root_path)
            self.sftp.put(path_item)
        except FileNotFoundError:
            rich_print_error("Error: [SFTP]: The 'root' folder couldn't be found on the remote host!")
            rich_print_error("Error: [SFTP]: Aborting uploading.")
        self.sftp.close()
        return None

    def list_plugins(self):
        """
        List all plugins in the 'plugins' folder on the sftp host

        :return: List of plugins in plugin folder
        """
        try:
            self.sftp.chdir(str(self.plugin_path))
            installed_plugins = self.sftp.listdir()
        except FileNotFoundError:
            rich_print_error("Error: [SFTP]: The 'plugins' folder couldn't be found on the remote host!")

        try:
            return installed_plugins
        except UnboundLocalError:
            rich_print_error("Error: [SFTP]: No plugins were found.")

    def list_files_in_server_root(self):
        """
        List all files in the root folder on the sftp host

        :returns: List of files in root folder
        """
        try:
            self.sftp.chdir(self.root_path)
            files_in_server_root = self.sftp.listdir()
        except FileNotFoundError:
            rich_print_error("Error: [SFTP]: The 'root' folder couldn't be found on the remote host!")
        try:
            return files_in_server_root
        except UnboundLocalError:
            rich_print_error("Error: [SFTP]: No Serverjar was found.")

    def download_plugin(self, file, dest) -> None:
        """
        Downloads a plugin file from the sftp host to the dest folder

        :param file: name of the plugin file
        :param dest: destination (on this system)

        :returns: None
        """
        self.sftp.cwd(str(self.plugin_path))
        current_directory = os.getcwd()
        os.chdir(dest)
        self.sftp.get(file)
        self.sftp.close()
        os.chdir(current_directory)
        return None

    def validate_plugin(self, file) -> bool:
        """
        Check if the file is a legitimate plugin file

        :param sftp: sftp connection
        param plugin_path: Path of the single plugin file

        :returns: If file is a plugin file or not 
        """
        self.create_connection()
        plugin_path = f"{self.plugin_path}/{file}"
        plugin_sftp_attribute = self.sftp.lstat(plugin_path)
        if stat.S_ISDIR(plugin_sftp_attribute.st_mode):
            return False
        elif re.search(r'.jar$', plugin_path):
            return True
        else:
            return False
        
    def delete_plugin(self, file):
        """
        Deletes a plugin from the plugins folder

        :param file: The name of the file to delete
        """
        self.sftp.remove(f"{self.plugin_path}/{file}")

    def delete_server_jar(self, file):
        """
        Deletes a plugin from the server root

        :param file: The name of the file to delete
        """
        self.sftp.remove(f"{self.root_path}/{file}")
