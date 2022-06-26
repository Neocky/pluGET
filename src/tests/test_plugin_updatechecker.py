import unittest

from src.plugin import plugin_updatechecker 


class TestCases(unittest.TestCase):
    def test_get_plugin_file_name(self):
        plugin_file_name = "LuckPerms-5.4.30.jar"
        plugin_file_name_cropped = "LuckPerms"
        result = plugin_updatechecker.get_plugin_file_name(plugin_file_name)
        self.assertEqual(result, plugin_file_name_cropped)
    
    def test_get_plugin_file_version(self):
        plugin_file_name = "LuckPerms-5.4.30.jar"
        plugin_version_cropped = "5.4.30"
        result = plugin_updatechecker.get_plugin_file_version(plugin_file_name)
        self.assertEqual(result, plugin_version_cropped)

    def test_get_plugin_version_without_letters(self):
        plugin_version = "VERSIONv5.4.30"
        plugin_version_cropped = "5.4.30"
        result = plugin_updatechecker.get_plugin_version_without_letters(plugin_version)
        self.assertEqual(result, plugin_version_cropped)

    def test_compare_plugin_version(self):
        result = plugin_updatechecker.compare_plugin_version("5.4.30", "5.4.0")
        result2 = plugin_updatechecker.compare_plugin_version("5.4.30", "8.7.60")
        result3 = plugin_updatechecker.compare_plugin_version("5.4.30", "5.4.30")
        self.assertEqual(result, True)
        self.assertEqual(result2, False)
        self.assertEqual(result3, False)
