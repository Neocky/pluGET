import os
import shutil
import re
from pathlib import Path

class local_server():
    def create_connection(self):
        """
        Does not do anything, placeholder for if this were a remote connection
        """
        pass

    def close_connection(self):
        """
        Does not do anything, placeholder for if this were a remote connection
        """
        pass

    def upload_plugin(self, file):
        """
        Moves a plugin to the plugins folder or seperate download folder

        :param path_item: Name of the item which should be moved

        :returns: None
        """
        if self.seperate_download_path is not False:
            path_upload_folder = self.seperate_download_path
        else:
            path_upload_folder = self.plugin_path
        shutil.copy(file, path_upload_folder)

    def upload_server_jar(self, file):
        """
        Moves a serverjar to the root folder of the server

        :param path_item: Name of the file which should be moved

        :returns: None
        """
        shutil.copy(file, self.root_path)

    def list_plugins(self):
        """
        Returns a list with all installed plugins in the plugin folder

        :returns: List of all plugins in plugin folder
        """
        return os.listdir(self.plugin_path)
    
    def list_server_root(self):
        """
        Returns a list with all files in the root folder of the server

        :returns: List of all files in root folder
        """
        return os.listdir(self.root_path)
    
    def download_plugin(self, file, dest):
        """
        Moves a plugin file from the plugins folder to the dest folder

        :param file: name of the plugin file
        :param dest: destination

        :returns None
        """
        shutil.copy(f"{self.plugin_path}/{file}", dest)

    def validate_plugin(self, plugin_file):
        """
        Check if a file is a legitimate plugin file

        :param ftp: ftp connection
        :param plugin_path: Path of file to check
        
        :returns: If file is a plugin file or not
        """
        plugin_attributes = True
        if not os.path.isfile(Path(f"{self.plugin_path}/{plugin_file}")):
            plugin_attributes = False
        elif not re.search(r'.jar$', plugin_file):
            plugin_attributes = False
        return plugin_attributes
        
    def delete_plugin(self, file):
        """
        Deletes a plugin from the plugins folder

        :param file: The name of the file to delete
        """
        os.remove(f"{self.plugin_path}/{file}")

    def delete_server_jar(self, file):
        """
        Deletes a plugin from the server root

        :param file: The name of the file to delete
        """
        os.remove(f"{self.root_path}/{file}")