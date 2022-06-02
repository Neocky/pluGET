import os
import re
from pathlib import Path

from utils.consoleoutput import oColors
from handlers.handle_config import configurationValues
from handlers.handle_sftp import createSFTPConnection, sftp_listAll
from handlers.handle_ftp import createFTPConnection, ftp_listAll
from plugin.plugin_updatechecker import getFileName, getFileVersion, getInstalledPlugin, createPluginList


def removePlugin(pluginToRemove):
    configValues = configurationValues()
    createPluginList()
    if not configValues.localPluginFolder:
        if not configValues.sftp_useSftp:
            ftp = createFTPConnection()
            pluginList = ftp_listAll(ftp)
        else:
            sftp = createSFTPConnection()
            pluginList = sftp_listAll(sftp)
    else:
        pluginList = os.listdir(configValues.pathToPluginFolder)
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
                if not configValues.localPluginFolder:
                    pluginPath = configValues.sftp_folderPath
                    pluginPath = f"{pluginPath}/{plugin}"
                    if not configValues.sftp_useSftp:
                        ftp = createFTPConnection()
                        ftp.delete(pluginPath)
                    else:
                        sftp = createSFTPConnection()
                        sftp.remove(pluginPath)
                    print(f"Removed: {fileName}")
                    i += 1
                    break
                else:
                    pluginPath = configValues.pathToPluginFolder
                    pluginPath = Path(f"{pluginPath}/{plugin}")
                    os.remove(pluginPath)
                    print(f"Removed: {fileName}")
                    i += 1
                    break
    except TypeError:
        print(oColors.brightRed + f"Aborted removing of: {pluginToRemove}." + oColors.standardWhite)
    if i == 0:
        print(oColors.brightRed + f"Couldn't remove plugin: {pluginToRemove}" + oColors.standardWhite)
