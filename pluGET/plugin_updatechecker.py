import os
import re
import requests

#from consoleoutput import consoleTitle, clearConsole
#from plugin_downloader import handleInput


def getInstalledPackages(pluginFolderPath):
    pluginList = os.listdir(pluginFolderPath)
    print(pluginList)
    for plugin in pluginList:
        print(plugin)
        getInstalledPluginVersion(plugin)


def getInstalledPluginVersion(pluginName):
    pluginNameFull = pluginName
    pluginVersion = re.search(r'([\d.]+[.jar]+)', pluginNameFull)
    pluginVersionFull = pluginVersion.group()
    pluginVersionString = pluginVersionFull.replace('.jar', '')
    pluginNameOnly = pluginNameFull.replace(pluginVersionFull, '')
    pluginNameOnly = pluginNameOnly[:-1]
    print(pluginNameOnly)
    print(pluginVersionString)
    response = requests.get("https://api.spiget.org/v2/search/resources/" + pluginNameOnly + "?field=name")
    #https://api.spiget.org/v2/search/resources/luckperms?field=name
    print("https://api.spiget.org/v2/search/resources/" + pluginNameOnly + "?field=name")
    packageName = response.json()
    i = 1
    for ressource in packageName:
        pName = ressource["name"]
        pID = ressource["id"]
        print(f"    [{i}] {pName}")
        i = i + 1

    # start query 
    # get id
    # search with id for all version upaates
    # get version that matches installed version
    # if match then download latest update
    # else get second query