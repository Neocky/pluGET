import os
import re

from utils.consoleoutput import oColors
from utils.web_request import doAPIRequest
from handlers.handle_config import checkConfig
from handlers.handle_sftp import createSFTPConnection, sftp_listAll
from plugin.plugin_downloader import getSpecificPackage


def createPluginList():
    global INSTALLEDPLUGINLIST
    INSTALLEDPLUGINLIST = []
    return INSTALLEDPLUGINLIST


def addToPluginList(pluginId, versionId, plugin_is_outdated):
    INSTALLEDPLUGINLIST.append([pluginId, versionId, plugin_is_outdated])


def getFileName(pluginName):
    pluginNameFull = pluginName
    pluginVersion = re.search(r'([\d.]+[.jar]+)', pluginNameFull)
    try:
        pluginVersionFull = pluginVersion.group()
    except AttributeError:
        pluginVersionFull = pluginVersion
    pluginNameOnlyy = pluginNameFull.replace(pluginVersionFull, '')
    pluginNameOnly = re.sub(r'(\-$)', '', pluginNameOnlyy)
    return pluginNameOnly


def getFileVersion(pluginName):
    pluginNameFull = pluginName
    pluginVersion = re.search(r'([\d.]+[.jar]+)', pluginNameFull)
    pluginVersionFull = pluginVersion.group()
    pluginVersionString = pluginVersionFull.replace('.jar', '')
    return pluginVersionString


def compareVersions(pluginId, pluginVersion):
    url = f"https://api.spiget.org/v2/resources/{pluginId}/versions/latest"
    latestUpdateSearch = doAPIRequest(url)
    versionLatestUpdate = latestUpdateSearch["name"]
    if pluginVersion != versionLatestUpdate:
        plugin_is_outdated = True
    else:
        plugin_is_outdated = False
    return plugin_is_outdated


def checkInstalledPackage(inputSelectedObject="all"):
    createPluginList()
    if not checkConfig().localPluginFolder:
        sftp = createSFTPConnection()
        pluginList = sftp_listAll(sftp)
    else:
        pluginList = os.listdir(checkConfig().pathToPluginFolder)
    i = 0
    oldPackages = 0
    print("Index / Name / Installed Version / Update available")
    try:
        for plugin in pluginList:
            try:
                fileName = getFileName(plugin)
                fileVersion = getFileVersion(plugin)
                pluginId = getInstalledPlugin(fileName, fileVersion)
            except TypeError:
                continue
            pluginIdStr = str(pluginId)

            if fileVersion == '':
                fileVersion = 'N/A'

            try:
                pluginIsOutdated = INSTALLEDPLUGINLIST[i][2]
            except IndexError:
                pluginIsOutdated = 'N/A'

            if pluginIsOutdated == True:
                oldPackages = oldPackages + 1

            if inputSelectedObject != "*":
                if inputSelectedObject != "all":
                    if inputSelectedObject == pluginIdStr or re.search(inputSelectedObject, fileName, re.IGNORECASE):
                        print(f"[{1}] {fileName} - {fileVersion} - {pluginIsOutdated}")
                        break
                else:
                    print(f"[{i+1}] {fileName} - {fileVersion} - {pluginIsOutdated}") # TODO find better way for the 2 else
            else:
                print(f"[{i+1}] {fileName} - {fileVersion} - {pluginIsOutdated}")

            i = i + 1
    except TypeError:
        print(oColors.brightRed + "Aborted checking for plugins." + oColors.standardWhite)
    print(f"Old packages: [{oldPackages}/{i}]")


def updateInstalledPackage(inputSelectedObject='all'):
    createPluginList()
    if not checkConfig().localPluginFolder:
        sftp = createSFTPConnection()
        pluginList = sftp_listAll(sftp)
    else:
        pluginList = os.listdir(checkConfig().pathToPluginFolder)
    i = 0
    pluginsUpdated = 0
    try:
        for plugin in pluginList:
            print(plugin)
            try:
                fileName = getFileName(plugin)
                fileVersion = getFileVersion(plugin)
                pluginId = getInstalledPlugin(fileName, fileVersion)
            except TypeError:
                continue
            pluginIdStr = str(pluginId)

            if pluginId == None:
                print(oColors.brightRed + "Couldn't find plugin id. Sorry :(" + oColors.standardWhite)
                continue

            if inputSelectedObject == pluginIdStr or re.search(inputSelectedObject, fileName, re.IGNORECASE):
                print(f"Updating: {fileName}")
                if not checkConfig().localPluginFolder:
                    pluginPath = checkConfig().sftp_folderPath
                    pluginPath = f"{pluginPath}\\{plugin}"
                    sftp = createSFTPConnection()
                    sftp.remove(pluginPath)
                    getSpecificPackage(pluginId, checkConfig().sftp_folderPath)
                    pluginsUpdated += 1
                else:
                    pluginPath = checkConfig().pathToPluginFolder
                    pluginPath = f"{pluginPath}\\{plugin}"
                    os.remove(pluginPath)
                    getSpecificPackage(pluginId, checkConfig().pathToPluginFolder)
                    pluginsUpdated += 1
                break

            if inputSelectedObject == 'all':
                if INSTALLEDPLUGINLIST[i][2] == True:
                    if not checkConfig().localPluginFolder:
                        pluginPath = checkConfig().sftp_folderPath
                        pluginPath = f"{pluginPath}\\{plugin}"
                        print("Deleting old plugin...")
                        sftp = createSFTPConnection()
                        sftp.remove(pluginPath)
                        print("Downloading new plugin...")
                        getSpecificPackage(pluginId, checkConfig().sftp_folderPath)
                        pluginsUpdated += 1

                    else:
                        pluginPath = checkConfig().pathToPluginFolder
                        pluginPath = f"{pluginPath}\\{plugin}"
                        print("Deleting old plugin...")
                        os.remove(pluginPath)
                        print("Downloading new plugin...")
                        getSpecificPackage(pluginId, checkConfig().pathToPluginFolder)
                        pluginsUpdated += 1
            i = i + 1
    except TypeError:
        print(oColors.brightRed + "Aborted updating for plugins." + oColors.standardWhite)
    print(f"[{pluginsUpdated}/{i}] Plugins updated")


def getInstalledPlugin(localFileName, localFileVersion):
    url = "https://api.spiget.org/v2/search/resources/" + localFileName + "?field=name"
    packageName = doAPIRequest(url)
    i = 1
    plugin_match_found = False
    pluginID = None
    for ressource in packageName:
        if plugin_match_found == True:
            break
        #pName = ressource["name"]
        pID = ressource["id"]
        url2 = f"https://api.spiget.org/v2/resources/{pID}/versions?size=100&sort=-name"
        packageVersions = doAPIRequest(url2)
        for updates in packageVersions:
            updateVersion = updates["name"]
            if localFileVersion == updateVersion:
                plugin_match_found = True
                pluginID = pID
                updateId = updates["id"]
                plugin_is_outdated = compareVersions(pID, updateVersion)
                addToPluginList(pID, updateId, plugin_is_outdated)
                break
        i = i + 1
    return pluginID


    # start query
    # get id
    # search with id for all version upates
    # get version that matches installed version
    # if match then download latest update
    # else get second query
