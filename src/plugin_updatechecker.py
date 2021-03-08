import os
import re

from consoleoutput import oColors
from plugin_downloader import getSpecificPackage #handleInput
from web_request import doAPIRequest
from handle_config import checkConfig


def createPluginList():
    global INSTALLEDPLUGINLIST
    INSTALLEDPLUGINLIST = []
    return INSTALLEDPLUGINLIST


def addToPluginList(pluginId, versionId, plugin_is_outdated):
    INSTALLEDPLUGINLIST.append([pluginId, versionId, plugin_is_outdated])


def getFileName(pluginName):
    pluginNameFull = pluginName
    pluginVersion = re.search(r'([\d.]+[.jar]+)', pluginNameFull)
    pluginVersionFull = pluginVersion.group()
    pluginNameOnly = pluginNameFull.replace(pluginVersionFull, '')
    pluginNameOnly = re.sub(r'(\-$)', '', pluginNameOnly)
    return pluginNameOnly


def getFileVersion(pluginName):
    #pluginVersionString = None
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


def checkInstalledPackage(pluginFolderPath, inputSelectedObject="all"):
    createPluginList()
    pluginList = os.listdir(pluginFolderPath)
    i = 0
    oldPackages = 0
    print("Index / Name / Installed Version / Update available")

    for plugin in pluginList:
        fileName = getFileName(plugin)
        fileVersion = getFileVersion(plugin)
        pluginId = getInstalledPlugin(fileName, fileVersion)
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
    print(f"Old packages: [{oldPackages}/{i}]")


def updateInstalledPackage(pluginFolderPath, inputSelectedObject='all'):
    createPluginList()
    pluginList = os.listdir(pluginFolderPath)
    print(pluginList)
    i = 0
    for plugin in pluginList:
        print(plugin)
        fileName = getFileName(plugin)
        fileVersion = getFileVersion(plugin)
        pluginId = getInstalledPlugin(fileName, fileVersion)
        pluginIdStr = str(pluginId)

        if pluginId == None:
            print(oColors.brightRed + "Couldn't find plugin id. Sorry :(" + oColors.standardWhite)
            continue

        if inputSelectedObject == pluginIdStr or re.search(inputSelectedObject, fileName, re.IGNORECASE):
            print(f"Updating: {fileName}")
            pluginPath = checkConfig().pathToPluginFolder
            pluginPath = f"{pluginPath}\\{plugin}"
            os.remove(pluginPath)
            getSpecificPackage(pluginId, checkConfig().pathToPluginFolder)
            break

        if inputSelectedObject == 'all':
            if INSTALLEDPLUGINLIST[i][2] == True:
                print("Deleting old plugin...")
                pluginPath = checkConfig().pathToPluginFolder
                pluginPath = f"{pluginPath}\\{plugin}"
                os.remove(pluginPath)
                print("Downloading new plugin...")
                getSpecificPackage(pluginId, checkConfig().pathToPluginFolder)
        i = i + 1
    #print(INSTALLEDPLUGINLIST[1][0])
        #getLatestPackageVersion(pluginID, r"C:\\Users\USER\Desktop\\plugins\\")


def getInstalledPlugin(localFileName, localFileVersion):
    url = "https://api.spiget.org/v2/search/resources/" + localFileName + "?field=name"
    packageName = doAPIRequest(url)
    #packageName = response.json()
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
