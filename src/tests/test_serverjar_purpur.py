import unittest

from src.serverjar import serverjar_purpur
from src.serverjar import serverjar_paper_velocity_waterfall

class TestCases(unittest.TestCase):
    def test_get_installed_serverjar_version(self):
        # purpur-1.19-40.jar -> 40
        serverjar_file_name = "purpur-1.19-40.jar"
        serverjar_version = "40"
        result = serverjar_paper_velocity_waterfall.get_installed_serverjar_version(serverjar_file_name)
        self.assertEqual(result, serverjar_version)


    def test_get_version_group(self):
        # 1.18.2 -> 1.18
        mc_version = "1.18.2"
        mc_version_group = "1.18.2"
        result = serverjar_paper_velocity_waterfall.get_version_group(mc_version)
        self.assertEqual(result, mc_version_group)


    def test_find_latest_available_version(self):
        # Get latest available purpur version for 1.15.2 which should be '606'
        file_server_jar_full_name = "purpur-1.15.2-40.jar"
        version_group = "1.15.2"
        result = serverjar_purpur.find_latest_available_version(version_group)
        self.assertEqual(result, str(606))


    def test_get_versions_behind(self):
        # 161 - 157 = 4
        serverjar_version = 157
        latest_version = 161
        result = serverjar_paper_velocity_waterfall.get_versions_behind(serverjar_version, latest_version)
        self.assertEqual(result, 4)


if __name__ == "__main__":
    unittest.main()
