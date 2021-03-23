import os
import re
import io
from zipfile import ZipFile
from urllib.error import HTTPError
from pathlib import Path
from rich.progress import track

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
    if pluginVersionString.endswith('.'):
        pluginVersionString = ''
    if pluginVersionString == '':
        pluginVersionString = eggCrackingJar(pluginNameFull)
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


def eggCrackingJar(localJarFileName):
    if not checkConfig().localPluginFolder:
        pluginPath = checkConfig().sftp_folderPath
    else:
        pluginPath = checkConfig().pathToPluginFolder
    pathToPluginJar = Path(f"{pluginPath}/{localJarFileName}")
    pluginVersion = ''
    with ZipFile(pathToPluginJar, 'r') as pluginJar:
        try:
            with io.TextIOWrapper(pluginJar.open('plugin.yml', 'r'), encoding="utf-8") as pluginYml:
                pluginYmlContentLine = pluginYml.readlines()
                for line in pluginYmlContentLine:
                    if "version: " in line:
                        pluginVersion = line.replace('version: ', '')
                        pluginVersion = pluginVersion.replace('\n', '')
                        break

        except FileNotFoundError:
            pluginVersion = ''
    return pluginVersion


def checkInstalledPackage(inputSelectedObject="all"):
    createPluginList()
    if not checkConfig().localPluginFolder:
        sftp = createSFTPConnection()
        pluginList = sftp_listAll(sftp)
    else:
        pluginList = os.listdir(checkConfig().pathToPluginFolder)
    i = 0
    oldPackages = 0
    print(oColors.brightBlack + f"Checking: {inputSelectedObject}" + oColors.standardWhite)
    print("┌─────┬────────────────────────────────┬──────────────┬───────────┬───────────────────┐")
    print("│ No. │ Name                           │ Installed V. │ Latest V. │ Update available  │")
    print("└─────┴────────────────────────────────┴──────────────┴───────────┴───────────────────┘")
    try:
        for plugin in track(pluginList, description="Checking for updates" ,transient=True, complete_style="cyan"):
            try:
                fileName = getFileName(plugin)
                fileVersion = getFileVersion(plugin)
                pluginId = getInstalledPlugin(fileName, fileVersion)
            except TypeError:
                i += 1
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
                    if pluginLatestVersion == 'N/A':
                        print(oColors.brightBlack + f" [{1}]".ljust(8), end='')
                    else:
                        print(f" [{1}]".ljust(8), end='')
                    print(f"{fileName}".ljust(33), end='')
                    print(f"{fileVersion}".ljust(15), end='')
                    print(f"{pluginLatestVersion}".ljust(12), end='')
                    print(f" {pluginIsOutdated}".ljust(5) + oColors.standardWhite)
                    break
            else:
                if pluginLatestVersion == 'N/A':
                    print(oColors.brightBlack + f" [{i+1}]".ljust(8), end='')
                else:
                    print(f" [{i+1}]".ljust(8), end='')
                print(f"{fileName}".ljust(33), end='')
                print(f"{fileVersion}".ljust(15), end='')
                print(f"{pluginLatestVersion}".ljust(12), end='')
                print(f" {pluginIsOutdated}".ljust(5) + oColors.standardWhite)

            i += 1
    except TypeError:
        print(oColors.brightRed + "Error occured: Aborted checking for updates." + oColors.standardWhite)
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
    indexNumberUpdated = 0
    print(oColors.brightBlack + f"Updating: {inputSelectedObject}" + oColors.standardWhite)
    print("┌─────┬────────────────────────────────┬────────────┬──────────┐")
    print("│ No. │ Name                           │ Old V.     │ New V.   │")
    print("└─────┴────────────────────────────────┴────────────┴──────────┘")
    try:
        for plugin in track(pluginList, description="Updating" ,transient=True, complete_style="red"):
            try:
                fileName = getFileName(plugin)
                fileVersion = getFileVersion(plugin)
                pluginId = getInstalledPlugin(fileName, fileVersion)
                latestVersion = getLatestPluginVersion(pluginId)
            except TypeError:
                i += 1
                continue
            except ValueError:
                i += 1
                continue
            pluginIdStr = str(pluginId)
            if pluginId == None or pluginId == '':
                print(oColors.brightRed + "Couldn't find plugin id. Sorry :(" + oColors.standardWhite)
                continue
            if inputSelectedObject == pluginIdStr or re.search(inputSelectedObject, fileName, re.IGNORECASE):
                if INSTALLEDPLUGINLIST[i][3] == True:
                    print(f" [{indexNumberUpdated+1}]".ljust(8), end='')
                    print(f"{fileName}".ljust(33), end='')
                    print(f"{fileVersion}".ljust(8), end='')
                    print("     ", end='')
                    print(f"{latestVersion}".ljust(8))

                    if not checkConfig().localPluginFolder:
                        if checkConfig().sftp_seperateDownloadPath is True:
                            pluginPath = checkConfig().sftp_pathToSeperateDownloadPath
                        else:
                            pluginPath = checkConfig().sftp_folderPath
                        pluginPath = Path(f"{pluginPath}/{plugin}")
                        sftp = createSFTPConnection()
                        indexNumberUpdated += 1
                        pluginsUpdated += 1
                        try:
                            getSpecificPackage(pluginId, checkConfig().sftp_folderPath)
                            if checkConfig().sftp_seperateDownloadPath is False:
                                sftp.remove(pluginPath)
                        except HTTPError as err:
                            print(oColors.brightRed +  f"Error: {err.code} - {err.reason}" + oColors.standardWhite)
                            pluginsUpdated -= 1
                        except FileNotFoundError:
                            print(oColors.brightRed +  "Error: Old plugin file coulnd't be deleted" + oColors.standardWhite)
                    else:
                        if checkConfig().seperateDownloadPath is True:
                            pluginPath = checkConfig().pathToSeperateDownloadPath
                        else:
                            pluginPath = checkConfig().pathToPluginFolder
                        pluginPath = Path(f"{pluginPath}/{plugin}")
                        indexNumberUpdated += 1
                        pluginsUpdated += 1
                        try:
                            getSpecificPackage(pluginId, checkConfig().pathToPluginFolder)
                            if checkConfig().seperateDownloadPath is False:
                                os.remove(pluginPath)
                        except HTTPError as err:
                            print(oColors.brightRed +  f"Error: {err.code} - {err.reason}" + oColors.standardWhite)
                            pluginsUpdated -= 1
                        except FileNotFoundError:
                            print(oColors.brightRed +  f"Error: Old plugin file coulnd't be deleted" + oColors.standardWhite)
                    break
                else:
                    print(f"{fileName} is already on {latestVersion}")
                    print(oColors.brightRed + "Aborting the update process."+ oColors.standardWhite)
                    break

            if inputSelectedObject == 'all':
                if INSTALLEDPLUGINLIST[i][3] == True:
                    print(f" [{indexNumberUpdated+1}]".ljust(8), end='')
                    print(f"{fileName}".ljust(33), end='')
                    print(f"{fileVersion}".ljust(8), end='')
                    print("     ", end='')
                    print(f"{latestVersion}".ljust(8))

                    if not checkConfig().localPluginFolder:
                        if checkConfig().sftp_seperateDownloadPath is True:
                            pluginPath = checkConfig().sftp_pathToSeperateDownloadPath
                        else:
                            pluginPath = checkConfig().sftp_folderPath
                        pluginPath = f"{pluginPath}/{plugin}"
                        sftp = createSFTPConnection()
                        indexNumberUpdated += 1
                        pluginsUpdated += 1
                        try:
                            getSpecificPackage(pluginId, checkConfig().sftp_folderPath)
                            if checkConfig().sftp_seperateDownloadPath is False:
                                sftp.remove(pluginPath)
                        except HTTPError as err:
                            print(oColors.brightRed +  f"Error: {err.code} - {err.reason}" + oColors.standardWhite)
                            pluginsUpdated -= 1
                        except FileNotFoundError:
                            print(oColors.brightRed +  f"Error: Old plugin file coulnd't be deleted" + oColors.standardWhite)

                    else:
                        if checkConfig().seperateDownloadPath is True:
                            pluginPath = checkConfig().pathToSeperateDownloadPath
                        else:
                            pluginPath = checkConfig().pathToPluginFolder
                        pluginPath = Path(f"{pluginPath}/{plugin}")
                        indexNumberUpdated += 1
                        pluginsUpdated += 1
                        try:
                            getSpecificPackage(pluginId, checkConfig().pathToPluginFolder)
                            if checkConfig().seperateDownloadPath is False:
                                os.remove(pluginPath)
                        except HTTPError as err:
                            print(oColors.brightRed +  f"Error: {err.code} - {err.reason}" + oColors.standardWhite)
                            pluginsUpdated -= 1
                        except FileNotFoundError:
                            print(oColors.brightRed +  f"Error: Old plugin file coulnd't be deleted" + oColors.standardWhite)

            i = i + 1
    except TypeError:
        print(oColors.brightRed + "Error occured: Aborted updating for plugins." + oColors.standardWhite)
    print(oColors.brightYellow + f"[{pluginsUpdated}/{i}] Plugins updated" + oColors.standardWhite)
    if inputSelectedObject =='all' and pluginsUpdated == 0:
        print(oColors.brightGreen + "All found plugins are on the latest version!" + oColors.standardWhite)


def getInstalledPlugin(localFileName, localFileVersion):
    url = "https://api.spiget.org/v2/search/resources/" + localFileName + "?field=name&sort=-downloads"
    packageName = doAPIRequest(url)
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
                return pluginID

    else:
        if plugin_match_found != True:
            pID = None
            updateId = None
            plugin_latest_version = None
            plugin_is_outdated = None
            addToPluginList(pID, updateId,  plugin_latest_version , plugin_is_outdated)

    return pluginID
