import os
import re

from utils.consoleoutput import oColors
from handlers.handle_config import checkConfig
from handlers.handle_sftp import createSFTPConnection, sftp_listAll
from plugin.plugin_updatechecker import getFileName, getFileVersion, getInstalledPlugin, createPluginList


def removePlugin(pluginToRemove):
    createPluginList()
    if not checkConfig().localPluginFolder:
        sftp = createSFTPConnection()
        pluginList = sftp_listAll(sftp)
    else:
        pluginList = os.listdir(checkConfig().pathToPluginFolder)
    i = 0
    try:
        for plugin in pluginList:
            try:
                fileName = getFileName(plugin)
                fileVersion = getFileVersion(plugin)
                pluginId = getInstalledPlugin(fileName, fileVersion)
            except TypeError:
                continue
            pluginIdStr = str(pluginId)

            if pluginToRemove == pluginIdStr or re.search(pluginToRemove, fileName, re.IGNORECASE):
                print(f"Removing: {fileName}")
                if not checkConfig().localPluginFolder:
                    pluginPath = checkConfig().sftp_folderPath
                    pluginPath = f"{pluginPath}\\{plugin}"
                    sftp = createSFTPConnection()
                    sftp.remove(pluginPath)
                    print(f"Removed: {fileName}")
                    i += 1
                    break
                else:
                    pluginPath = checkConfig().pathToPluginFolder
                    pluginPath = f"{pluginPath}\\{plugin}"
                    os.remove(pluginPath)
                    print(f"Removed: {fileName}")
                    i += 1
                    break
    except TypeError:
        print(oColors.brightRed + f"Aborted removing of: {pluginToRemove}." + oColors.standardWhite)
    if i == 0:
        print(oColors.brightRed + f"Couldn't remove plugin: {pluginToRemove}" + oColors.standardWhite)
