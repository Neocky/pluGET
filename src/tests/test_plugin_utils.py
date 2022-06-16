import unittest
from src.plugin import plugin_downloader
from src.utils import utilities


class TestCases(unittest.TestCase):
    def test_handle_regex_package_name(self):
        plugin_name = "[1.13-5.49 ❤] >|> SUPERB Plugin <<💥| Now 150% OFF IN WINTER SALE IN SUMMER???"
        plugin_name_cropped = "SUPERBPlugin"
        result = plugin_downloader.handle_regex_package_name(plugin_name)
        self.assertEqual(result, plugin_name_cropped)


    def test_get_version_id(self):
        # 1234 -> "AntiPickup" in Version 1.4.1
        result = plugin_downloader.get_version_id("1234", "1.4.1")
        self.assertEqual(result, 43779)


    def test_get_version_name(self):
        # 43779 -> "1.4.1" from AntiPickup
        result = plugin_downloader.get_version_name("1234", 43779)
        self.assertEqual(result, "1.4.1")


    def test_get_download_path(self):
        # local plugin folder
        class config_values_local:
            connection = "local"
            local_seperate_download_path = True
            local_path_to_seperate_download_path = "/local/path/plugins"
        result=plugin_downloader.get_download_path(config_values_local)
        self.assertEqual(result, config_values_local.local_path_to_seperate_download_path)

        # plugin folder over sftp
        class config_values_sftp:
            connection = "sftp"
            remote_seperate_download_path = True
            remote_path_to_seperate_download_path = "/sftp/path/plugins"
        result=plugin_downloader.get_download_path(config_values_sftp)
        self.assertEqual(result, config_values_sftp.remote_path_to_seperate_download_path)

        # plugin folder over ftp
        class config_values_ftp:
            connection = "ftp"
            remote_seperate_download_path = True
            remote_path_to_seperate_download_path = "/ftp/path/plugins"
        result=plugin_downloader.get_download_path(config_values_ftp)
        self.assertEqual(result, config_values_ftp.remote_path_to_seperate_download_path)

    
    def test_convert_file_size_down(self):
        result= utilities.convert_file_size_down(100000)
        self.assertEqual(result, 97.66)
    

if __name__ == "__main__":
    unittest.main()
