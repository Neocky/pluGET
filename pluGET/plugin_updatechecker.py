import os
import re
import requests

#from consoleoutput import consoleTitle, clearConsole
from plugin_downloader import getLatestPackageVersion #handleInput


# as seen on https://pythonguides.com/create-list-in-python/
class installedPlugin:
    def __init__(self, pluginId, plugin_is_outdated):
        self.pluginId = pluginId
        self.plugin_is_outdated = plugin_is_outdated



def getFileName(pluginName):
    pluginNameFull = pluginName
    pluginVersion = re.search(r'([\d.]+[.jar]+)', pluginNameFull)
    pluginVersionFull = pluginVersion.group()
    pluginNameOnly = pluginNameFull.replace(pluginVersionFull, '')
    pluginNameOnly = pluginNameOnly[:-1]
    return pluginNameOnly


def getFileVersion(pluginName):
    pluginNameFull = pluginName
    pluginVersion = re.search(r'([\d.]+[.jar]+)', pluginNameFull)
    pluginVersionFull = pluginVersion.group()
    pluginVersionString = pluginVersionFull.replace('.jar', '')
    return pluginVersionString

# not yet implemented
def compareVersions(pluginVersion, pluginId, updateId):
    latestUpdateSearch = requests.get(f"https://api.spiget.org/v2/resources/{pluginId}/versions/{updateId}")
    versionLatestUpdate = latestUpdateSearch["name"]
    if pluginVersion != versionLatestUpdate:
        plugin_is_outdated = True
    else:
        plugin_is_outdated = False
    return plugin_is_outdated


def getInstalledPackages(pluginFolderPath):
    list = []
    
    pluginList = os.listdir(pluginFolderPath)
    print(pluginList)
    for plugin in pluginList:
        print(plugin)
        fileName = getFileName(plugin)
        fileVersion = getFileVersion(plugin)
        pluginId = getInstalledPluginVersion(fileName, fileVersion)
        list.append( installedPlugin(pluginId, plugin_is_outdated))
        if pluginId == None:
            print("Couldn't find plugin id. Sorry :(")
            continue

        #getLatestPackageVersion(pluginID, r"C:\\Users\USER\Desktop\\plugins\\")


def getInstalledPluginVersion(localFileName, localFileVersion):
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
                print(updates["id"])
                print("Found match")
                print(pID)
                break
        i = i + 1
    return pluginID


    # start query 
    # get id
    # search with id for all version upates
    # get version that matches installed version
    # if match then download latest update
    # else get second query