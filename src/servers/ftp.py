import os
import sys
import ftplib
import re
from pathlib import Path
from src.utils.console_output import rich_print_error

class ftp_server():
    def create_connection(self):
        """
        Creates a connection to the ftp server with the given values in the config
        """
        try:
            ftp = ftplib.FTP()
            ftp.connect(self.server, self.port)
            ftp.login(self.username, self.password)
            self.ftp = ftp
        except UnboundLocalError:
            rich_print_error("Error: [SFTP]: Check your config file!")
            rich_print_error("Exiting program...")
            sys.exit()
    
    def close_connection(self):
        """
        Closes the ftp connection
        """
        self.ftp.close()

    def upload_plugin(self, path_item) -> None:
        """
        Uploads a plugin to the plugins folder or seperate download folder

        :param path_item: Name of the item which should be uploaded

        :returns: None
        """
        if self.seperate_download_path is not False:
            path_upload_folder = self.seperate_download_path
        else:
            path_upload_folder = self.plugin_path
        try:
            self.ftp.cwd(path_upload_folder)
            with open (path_item, 'rb') as plugin_file:
                self.ftp.storbinary('STOR '+ str(path_item), plugin_file)
        except FileNotFoundError:
            rich_print_error("Error: [FTP]: The 'plugins' folder couldn't be found on the remote host!")
            rich_print_error("Error: [FTP]: Aborting uploading.")
        return None

    def upload_server_jar(self, path_item) -> None:
        """
        Uploads a serverjar to the root folder of the ftp host

        :param path_item: Name of the file which should be uploaded

        :returns: None
        """
        try:
            self.ftp.cwd(self.root_path)
            with open (path_item, 'rb') as server_jar:
                self.ftp.storbinary('STOR '+ str(path_item), server_jar)
        except FileNotFoundError:
            rich_print_error("Error: [FTP]: The 'root' folder couldn't be found on the remote host!")
            rich_print_error("Error: [FTP]: Aborting uploading.")
        return None

    def list_plugins(self):
        """
        Returns a list with all installed plugins in the plugin folder of the ftp host

        :returns: List of all plugins in plugin folder
        """
        try:
            self.ftp.cwd(self.plugin_path)
            installed_plugins = self.ftp.nlst()
        except FileNotFoundError:
            rich_print_error("Error: [FTP]: The 'plugins' folder couldn't be found on the remote host!")

        try:
            return installed_plugins
        except UnboundLocalError:
            rich_print_error("Error: [FTP]: No plugins were found.")

    def list_server_root(self):
        """
        Returns a list with all files in the root folder of the ftp host

        :returns: List of all files in root folder
        """
        try:
            self.ftp.cwd(self.server_root)
            filesInServerRoot = self.ftp.nlst()
        except FileNotFoundError:
            rich_print_error("Error: [FTP]: The 'root' folder couldn't be found on the remote host!")

        try:
            return filesInServerRoot
        except UnboundLocalError:
            rich_print_error("Error: [FTP]: No Serverjar was found.")

    def download_plugin(self, file, dest) -> None:
        """
        Downloads a plugin file from the sftp host to the dest folder

        :param file: name of the plugin file
        :param dest: destination (on this system)

        :returns None
        """
        self.ftp.cwd(self.plugin_path)
        filedata = open(dest,'wb')
        self.ftp.retrbinary('RETR '+file, filedata.write)
        filedata.close()
        self.ftp.quit()
        return None

    def validate_file_attributes(self, file) -> bool:
        """
        Check if a file is a legitimate plugin file

        :param ftp: ftp connection
        :param plugin_path: Path of file to check
        
        :returns: If file is a plugin file or not
        """
        plugin_path = f"{self.plugin_path}/{file}"
        if self.ftp.nlst(plugin_path) == [plugin_path] is False:
            return False
        if re.search(r'.jar$', plugin_path):
            return True
        else:
            return False
        
    def delete_plugin(self, file):
        """
        Deletes a plugin from the plugins folder

        :param file: The name of the file to delete
        """
        self.ftp.delete(f"{self.plugin_path}/{file}")

    def delete_server_jar(self, file):
        """
        Deletes a plugin from the server root

        :param file: The name of the file to delete
        """
        self.ftp.delete(f"{self.root_path}/{file}")
