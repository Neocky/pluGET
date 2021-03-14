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


def addToPluginList(pluginId, versionId, plugin_latest_version, plugin_is_outdated):
    INSTALLEDPLUGINLIST.append([pluginId, versionId, plugin_latest_version, plugin_is_outdated])


def getFileName(pluginName):
    pluginNameFull = pluginName
    pluginVersion = re.search(r'([\d.]+[.jar]+)', pluginNameFull)
    try:
        pluginVersionFull = pluginVersion.group()
    except AttributeError:
        pluginVersionFull = pluginVersion
    pluginNameOnlyy = pluginNameFull.replace(pluginVersionFull, '')
    pluginNameOnly = re.sub(r'(\-$)', '', pluginNameOnlyy)
    pluginNameOnlyy = re.sub(r'(\-v$)', '', pluginNameOnly)
    return pluginNameOnlyy


def getFileVersion(pluginName):
    pluginNameFull = pluginName
    pluginVersion = re.search(r'([\d.]+[.jar]+)', pluginNameFull)
    pluginVersionFull = pluginVersion.group()
    pluginVersionString = pluginVersionFull.replace('.jar', '')
    return pluginVersionString


def getLatestPluginVersion(pluginId):
    url = f"https://api.spiget.org/v2/resources/{pluginId}/versions/latest"
    latestUpdateSearch = doAPIRequest(url)
    versionLatestUpdate = latestUpdateSearch["name"]
    return versionLatestUpdate


def compareVersions(plugin_latest_version, pluginVersion):
    if pluginVersion < plugin_latest_version:
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
    print(f"Checking: {inputSelectedObject}")
    print("Index | Name                           | Installed V. | Latest V. |  Update available")
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
                pluginLatestVersion = INSTALLEDPLUGINLIST[i][2]
            except IndexError:
                pluginLatestVersion = 'N/A'
            
            if pluginLatestVersion == None:
                pluginLatestVersion = 'N/A'

            try:
                pluginIsOutdated = INSTALLEDPLUGINLIST[i][3]
            except IndexError:
                pluginIsOutdated = 'N/A'

            if pluginIsOutdated == None:
                pluginIsOutdated = 'N/A'

            if pluginIsOutdated == True:
                oldPackages = oldPackages + 1

            if inputSelectedObject != "*" and inputSelectedObject != "all":
                if inputSelectedObject == pluginIdStr or re.search(inputSelectedObject, fileName, re.IGNORECASE):
                    print(f" [{1}]".ljust(8), end='')
                    print(f"{fileName}".ljust(33), end='')
                    print(f"{fileVersion}".ljust(15), end='')
                    print(f"{pluginLatestVersion}".ljust(12), end='')
                    print(f" {pluginIsOutdated}".ljust(5))
                    break
            else:
                print(f" [{i+1}]".ljust(8), end='')
                print(f"{fileName}".ljust(33), end='')
                print(f"{fileVersion}".ljust(15), end='')
                print(f"{pluginLatestVersion}".ljust(12), end='')
                print(f" {pluginIsOutdated}".ljust(5))

            i = i + 1
    except TypeError:
        print(oColors.brightRed + "Aborted checking for plugins." + oColors.standardWhite)
    print(oColors.brightYellow + f"Old packages: [{oldPackages}/{i}]" + oColors.standardWhite)


def updateInstalledPackage(inputSelectedObject='all'):
    createPluginList()
    if not checkConfig().localPluginFolder:
        sftp = createSFTPConnection()
        pluginList = sftp_listAll(sftp)
    else:
        pluginList = os.listdir(checkConfig().pathToPluginFolder)
    i = 0
    pluginsUpdated = 0
    print(f"Updating: {inputSelectedObject}")
    print("Index | Name                        |   Old V.   |   New V.")
    try:
        for plugin in pluginList:
            try:
                fileName = getFileName(plugin)
                fileVersion = getFileVersion(plugin)
                pluginId = getInstalledPlugin(fileName, fileVersion)
                latestVersion = getLatestPluginVersion(pluginId)
            except TypeError:
                continue
            except ValueError:
                continue
            pluginIdStr = str(pluginId)

            if pluginId == None:
                print(oColors.brightRed + "Couldn't find plugin id. Sorry :(" + oColors.standardWhite)
                continue

            if inputSelectedObject == pluginIdStr or re.search(inputSelectedObject, fileName, re.IGNORECASE):
                if INSTALLEDPLUGINLIST[i][3] == True:
                    print(f" [{pluginsUpdated+1}]".ljust(8), end='')
                    print(f"{fileName}".ljust(30), end='')
                    print(f"{fileVersion}".ljust(8), end='')
                    print("     ", end='')
                    print(f"{latestVersion}".ljust(8))

                    if not checkConfig().localPluginFolder:
                        pluginPath = checkConfig().sftp_folderPath
                        pluginPath = f"{pluginPath}\\{plugin}"
                        sftp = createSFTPConnection()
                        sftp.remove(pluginPath)
                        getSpecificPackage(pluginId, checkConfig().sftp_folderPath)
                        pluginsUpdated += 1
                    else:
                        if checkConfig().seperateDownloadPath is True:
                            pluginPath = checkConfig().pathToSeperateDownloadPath
                        else:
                            pluginPath = checkConfig().pathToPluginFolder
                        pluginPath = f"{pluginPath}\\{plugin}"
                        os.remove(pluginPath)
                        getSpecificPackage(pluginId, checkConfig().pathToPluginFolder)
                        pluginsUpdated += 1
                    break
                else:
                    print(f"{fileName} is already on {latestVersion}")
                    print(oColors.brightRed + "Aborting the update process."+ oColors.standardWhite)
                    break

            if inputSelectedObject == 'all':
                if INSTALLEDPLUGINLIST[i][3] == True:
                    print(f" [{pluginsUpdated+1}]".ljust(8), end='')
                    print(f"{fileName}".ljust(30), end='')
                    print(f"{fileVersion}".ljust(8), end='')
                    print("     ", end='')
                    print(f"{latestVersion}".ljust(8))

                    if not checkConfig().localPluginFolder:
                        if checkConfig().sftp_seperateDownloadPath is True:
                            pluginPath = checkConfig().sftp_pathToSeperateDownloadPath
                        else:
                            pluginPath = checkConfig().sftp_folderPath
                        pluginPath = checkConfig().sftp_folderPath
                        pluginPath = f"{pluginPath}\\{plugin}"
                        sftp = createSFTPConnection()
                        sftp.remove(pluginPath)
                        getSpecificPackage(pluginId, checkConfig().sftp_folderPath)
                        pluginsUpdated += 1

                    else:
                        if checkConfig().seperateDownloadPath is True:
                            pluginPath = checkConfig().pathToSeperateDownloadPath
                        else:
                            pluginPath = checkConfig().pathToPluginFolder
                        pluginPath = f"{pluginPath}\\{plugin}"
                        os.remove(pluginPath)
                        getSpecificPackage(pluginId, checkConfig().pathToPluginFolder)
                        pluginsUpdated += 1
            i = i + 1
    except TypeError:
        print(oColors.brightRed + "Aborted updating for plugins." + oColors.standardWhite)
    print(f"[{pluginsUpdated}/{i}] Plugins updated")
    if inputSelectedObject =='all' and pluginsUpdated == 0:
        print(oColors.brightGreen + "All plugins are on the latest version!" + oColors.standardWhite)


def getInstalledPlugin(localFileName, localFileVersion):
    url = "https://api.spiget.org/v2/search/resources/" + localFileName + "?field=name&sort=-downloads"
    packageName = doAPIRequest(url)
    i = 1
    plugin_match_found = False
    pluginID = None
    for ressource in packageName:
        if plugin_match_found == True:
            break

        pID = ressource["id"]
        url2 = f"https://api.spiget.org/v2/resources/{pID}/versions?size=100&sort=-name"
        packageVersions = doAPIRequest(url2)
        for updates in packageVersions:
            updateVersion = updates["name"]
            if localFileVersion in updateVersion:
                plugin_match_found = True
                pluginID = pID
                updateId = updates["id"]
                plugin_latest_version = getLatestPluginVersion(pID)
                plugin_is_outdated = compareVersions(plugin_latest_version, updateVersion)
                addToPluginList(pID, updateId,  plugin_latest_version , plugin_is_outdated)
                break

        i = i + 1
    else:
        if plugin_match_found != True:
            pID = None
            updateId = None
            plugin_latest_version = None
            plugin_is_outdated = None
            addToPluginList(pID, updateId,  plugin_latest_version , plugin_is_outdated)

    return pluginID


    # start query
    # get id
    # search with id for all version upates
    # get version that matches installed version
    # if match then download latest update
    # else get second query
