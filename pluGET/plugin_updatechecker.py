import os
import re
import requests

from consoleoutput import oColors #consoleTitle, clearConsole
from plugin_downloader import getLatestPackageVersion #handleInput


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
    responseUpdateSearch = requests.get(f"https://api.spiget.org/v2/resources/{pluginId}/versions/latest")
    latestUpdateSearch = responseUpdateSearch.json()
    versionLatestUpdate = latestUpdateSearch["name"]
    print(pluginVersion)
    print(versionLatestUpdate)
    if pluginVersion != versionLatestUpdate:
        plugin_is_outdated = True
    else:
        plugin_is_outdated = False
    return plugin_is_outdated


def getInstalledPackages(pluginFolderPath):
    createPluginList()
    pluginList = os.listdir(pluginFolderPath)
    print(pluginList)
    i = 0
    for plugin in pluginList:
        print(plugin)
        fileName = getFileName(plugin)
        fileVersion = getFileVersion(plugin)
        pluginId = getInstalledPlugin(fileName, fileVersion)

        print(f"name: {fileName}")
        print(f"version: {fileVersion}")

        print(INSTALLEDPLUGINLIST)
        
        if pluginId == None:
            print(oColors.brightRed + "Couldn't find plugin id. Sorry :(" + oColors.standardWhite)
            continue
        if INSTALLEDPLUGINLIST[i][2] == True:
            getLatestPackageVersion(pluginId, r"C:\\Users\\USER\\Desktop\\plugins\\")
        os.remove(f"C:\\Users\USER\\Desktop\\plugins\\{plugin}")
    print(INSTALLEDPLUGINLIST[1][0])
        #getLatestPackageVersion(pluginID, r"C:\\Users\USER\Desktop\\plugins\\")


def getInstalledPlugin(localFileName, localFileVersion):
    response = requests.get("https://api.spiget.org/v2/search/resources/" + localFileName + "?field=name")
    #https://api.spiget.org/v2/search/resources/luckperms?field=name
    print("https://api.spiget.org/v2/search/resources/" + localFileName + "?field=name")
    packageName = response.json()
    i = 1
    plugin_match_found = False
    pluginID = None
    for ressource in packageName:
        if plugin_match_found == True:
            break
        pName = ressource["name"]
        pID = ressource["id"]
        print(f"    [{i}] {pName} - {pID}")
        response2 = requests.get(f"https://api.spiget.org/v2/resources/{pID}/versions?size=100&sort=-name")
        packageVersions = response2.json()
        for updates in packageVersions:
            updateVersion = updates["name"]
            if localFileVersion == updateVersion:
                plugin_match_found = True
                pluginID = pID
                updateId = updates["id"]
                plugin_is_outdated = compareVersions(pID, updateVersion)
                addToPluginList(pID, updateId, plugin_is_outdated)
                print(updateId)
                print(pID)
                print("Found match")
                break
        i = i + 1
    return pluginID


    # start query 
    # get id
    # search with id for all version upates
    # get version that matches installed version
    # if match then download latest update
    # else get second query