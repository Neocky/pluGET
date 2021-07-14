import os
import re
import io
import base64
from zipfile import ZipFile
from urllib.error import HTTPError
from pathlib import Path
from rich.progress import track

from utils.consoleoutput import oColors
from utils.web_request import doAPIRequest
from handlers.handle_config import configurationValues
from handlers.handle_sftp import createSFTPConnection, sftp_listAll, sftp_downloadFile, sftp_validateFileAttributes
from handlers.handle_ftp import createFTPConnection, ftp_listAll, ftp_downloadFile, ftp_validateFileAttributes
from plugin.plugin_downloader import getSpecificPackage
from utils.utilities import createTempPluginFolder, deleteTempPluginFolder


def createPluginList():
    global INSTALLEDPLUGINLIST
    INSTALLEDPLUGINLIST = []
    return INSTALLEDPLUGINLIST


def addToPluginList(localFileName, pluginId, versionId, plugin_latest_version, plugin_is_outdated):
    INSTALLEDPLUGINLIST.append([localFileName, pluginId, versionId, plugin_latest_version, plugin_is_outdated])


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
        pluginVersionString = eggCrackingJar(pluginNameFull, 'version')
    return pluginVersionString


def getLatestPluginVersion(pluginId):
    url = f"https://api.spiget.org/v2/resources/{pluginId}/versions/latest"
    latestUpdateSearch = doAPIRequest(url)
    versionLatestUpdate = latestUpdateSearch["name"]
    return versionLatestUpdate


def getUpdateDescription(pluginId):
    url = f"https://api.spiget.org/v2/resources/{pluginId}/updates?size=1&sort=-date"
    latestDescriptionSearch = doAPIRequest(url)
    versionLatestDescription = latestDescriptionSearch[0]["description"]
    versionLatestDescription = base64.b64decode(versionLatestDescription)
    versionLatestDescriptionText =versionLatestDescription.decode('utf-8')
    htmlRegex = re.compile('<.*?>')
    versionLatestDescriptionText = re.sub(htmlRegex, '', versionLatestDescriptionText)
    linesChangelogDescription = versionLatestDescriptionText.split("\n")
    nonEmptyLines = [line for line in linesChangelogDescription if line.strip() != ""]
    stringnonEmptyLines = ""
    for line in nonEmptyLines:
        stringnonEmptyLines += line + "\n"
    stringnonEmptyLines = stringnonEmptyLines[:-1]
    return stringnonEmptyLines


def versionTuple(versionString):
    return tuple(map(int, (versionString.split("."))))


def getVersionWithoutLetters(versionString):
    return re.sub(r'([A-Za-z]*)', '', versionString)


def compareVersions(plugin_latest_version, pluginVersion):
    try:
        pluginVersionTuple = versionTuple(getVersionWithoutLetters(pluginVersion))
        plugin_latest_versionTuple = versionTuple(getVersionWithoutLetters(plugin_latest_version))
    except ValueError:
        return False
    if pluginVersionTuple < plugin_latest_versionTuple:
        return True
    else:
        return False


def eggCrackingJar(localJarFileName, searchMode):
    configValues = configurationValues()
    if not configValues.localPluginFolder:
        tempPluginFolderPath = createTempPluginFolder()
        if configValues.sftp_useSftp:
            sftp = createSFTPConnection()
            pathToPluginJar = Path(f"{tempPluginFolderPath}/{localJarFileName}")
            sftp_downloadFile(sftp, pathToPluginJar, localJarFileName)
        else:
            ftp = createFTPConnection()
            pathToPluginJar = Path(f"{tempPluginFolderPath}/{localJarFileName}")
            ftp_downloadFile(ftp, pathToPluginJar, localJarFileName)
    else:
        pluginPath = configValues.pathToPluginFolder
        pathToPluginJar = Path(f"{pluginPath}/{localJarFileName}")
    pluginVersion = ''
    pluginName = ''
    with ZipFile(pathToPluginJar, 'r') as pluginJar:
        try:
            with io.TextIOWrapper(pluginJar.open('plugin.yml', 'r'), encoding="utf-8") as pluginYml:
                pluginYmlContentLine = pluginYml.readlines()
                for line in pluginYmlContentLine:
                    if searchMode == 'version':
                        if re.match(r'^\s*?version: ', line):
                            pluginVersion = re.sub(r'^\s*?version: ', '', line)
                            pluginVersion = pluginVersion.replace('\n', '')
                            pluginVersion = pluginVersion.replace("'", '')
                            pluginVersion = pluginVersion.replace('"', '')
                    elif searchMode == 'name':
                        if re.match(r'^\s*?name: ', line):
                            pluginName = re.sub(r'^\s*?name: ', '', line)
                            pluginName = pluginName.replace('\n', '')
                            pluginName = pluginName.replace("'", '')
                            pluginName = pluginName.replace('"', '')

        except FileNotFoundError:
            pluginVersion = ''
            pluginName = ''
        except KeyError:
            pluginVersion = ''
            pluginName = ''
    if not configValues.localPluginFolder:
        deleteTempPluginFolder(tempPluginFolderPath)
    if searchMode == 'version':
        return pluginVersion
    if searchMode == 'name':
        return pluginName


def checkInstalledPackage(inputSelectedObject="all", inputOptionalParam=None):
    configValues = configurationValues()
    createPluginList()
    pluginFolderPath = configValues.pathToPluginFolder
    if not configValues.localPluginFolder:
        if configValues.sftp_useSftp:
            connection = createSFTPConnection()
            pluginList = sftp_listAll(connection)
        else:
            connection = createFTPConnection()
            pluginList = ftp_listAll(connection)
    else:
        pluginList = os.listdir(pluginFolderPath)

    i = 0
    oldPlugins = 0
    print(oColors.brightBlack + f"Checking: {inputSelectedObject}" + oColors.standardWhite)
    if inputOptionalParam != "changelog":
        print(oColors.brightBlack + f"Use 'check {inputSelectedObject} changelog' to get the latest changelog from plugins" + oColors.standardWhite)
    print("┌─────┬────────────────────────────────┬──────────────┬──────────────┐")
    print("│ No. │ Name                           │ Installed V. │ Latest V.    │")
    print("└─────┴────────────────────────────────┴──────────────┴──────────────┘")
    try:
        for plugin in track(pluginList, description="Checking for updates" ,transient=True, complete_style="bright_yellow"):
            if not configValues.localPluginFolder:
                pluginFile = f"{configValues.sftp_folderPath}/{plugin}"
                if configValues.sftp_useSftp:
                    pluginAttributes = sftp_validateFileAttributes(connection, pluginFile)
                    if pluginAttributes == False:
                        continue
                else:
                    pluginAttributes = ftp_validateFileAttributes(connection, pluginFile)
                    if pluginAttributes == False:
                        continue
            else:
                if not os.path.isfile(Path(f"{pluginFolderPath}/{plugin}")):
                    continue
                if not re.search(r'.jar$', plugin):
                    continue
            try:
                fileName = getFileName(plugin)
                fileVersion = getFileVersion(plugin)
                pluginId = getInstalledPlugin(fileName, fileVersion, plugin)
            except TypeError:
                continue

            pluginIdStr = str(pluginId)
            if fileVersion == '':
                fileVersion = 'N/A'
            try:
                pluginLatestVersion = INSTALLEDPLUGINLIST[i][3]
            except IndexError:
                pluginLatestVersion = 'N/A'

            if pluginLatestVersion == None:
                pluginLatestVersion = 'N/A'

            try:
                pluginIsOutdated = INSTALLEDPLUGINLIST[i][4]
            except IndexError:
                pluginIsOutdated = 'N/A'

            if pluginIsOutdated == None:
                pluginIsOutdated = 'N/A'

            if pluginIsOutdated == True:
                oldPlugins = oldPlugins + 1

            if re.search(r'.jar$', fileName):
                fileName = eggCrackingJar(plugin, "name")

            if inputSelectedObject != "all" and inputSelectedObject != "*":
                if inputSelectedObject != pluginIdStr or not re.search(inputSelectedObject, fileName, re.IGNORECASE):
                    i += 1
                    continue

            if inputSelectedObject == "all" or inputSelectedObject != "*" or inputSelectedObject != "all":
                if inputSelectedObject == pluginIdStr or re.search(inputSelectedObject, fileName, re.IGNORECASE):
                    if pluginLatestVersion == 'N/A':
                        print(oColors.brightBlack + f" [{1}]".rjust(6), end='')
                    else:
                        print(f" [{1}]".rjust(6), end='')
                else:
                    if pluginLatestVersion == 'N/A':
                        print(oColors.brightBlack + f" [{i+1}]".rjust(6), end='')
                    else:
                        print(f" [{i+1}]".rjust(6), end='')
                print("  ", end='')
                if pluginIsOutdated == True:
                    print(oColors.brightGreen + f"{fileName}".ljust(33) + oColors.standardWhite, end='')
                elif pluginIsOutdated == False:
                    print(oColors.brightRed + f"{fileName}".ljust(33) + oColors.standardWhite, end='')
                else:
                    print(f"{fileName}".ljust(33), end='')

                print(f"{fileVersion}".ljust(15), end='')
                print(f"{pluginLatestVersion}".ljust(15))
                if (inputOptionalParam == "changelog" and pluginLatestVersion != 'N/A'):
                    print(oColors.brightYellow + f"CHANGELOG {fileName}:" + oColors.standardWhite)
                    description = getUpdateDescription(pluginId)
                    print(description)
                    print()
                if inputSelectedObject == pluginIdStr or re.search(inputSelectedObject, fileName, re.IGNORECASE):
                    break
            else:
                print(oColors.brightRed + "Wrong input! Use 'check all' to check every plugin for updates!" + oColors.standardWhite)
                break

            i += 1
    except TypeError:
        print(oColors.brightRed + "Error occured: Aborted checking for updates." + oColors.standardWhite)
    print(oColors.brightYellow + f"Outdated plugins: [{oldPlugins}/{i}]" + oColors.standardWhite)


def updateInstalledPackage(inputSelectedObject='all'):
    configValues = configurationValues()
    if not configValues.localPluginFolder:
        if configValues.sftp_useSftp:
            connection = createSFTPConnection()
        else:
            connection = createFTPConnection()

    try:
        print(oColors.brightBlack + "Selected plugins with available Updates:" + oColors.standardWhite)
        if inputSelectedObject == "all" or inputSelectedObject == "*":
            for pluginIndex in range(len(INSTALLEDPLUGINLIST)):
                if INSTALLEDPLUGINLIST[pluginIndex][4] == True:
                    fileName = getFileName(INSTALLEDPLUGINLIST[pluginIndex][0])
                    print(fileName, end=' ')
        else:
            print(inputSelectedObject, end=' ')

        print()
        updateConfirmation = input("Update these plugins [y/n] ? ")
        if str.lower(updateConfirmation) != "y":
            print(oColors.brightRed + "Aborting the update process."+ oColors.standardWhite)
            return False

    except NameError:
        print(oColors.brightRed + "Check for updates before updating plugins with: 'check all'" + oColors.standardWhite)
        print(oColors.brightRed + "Started checking for updates..." + oColors.standardWhite)
        checkInstalledPackage()
        print(oColors.brightRed + f"Please input 'update {inputSelectedObject}' again!" + oColors.standardWhite)
        return False

    i = 0
    pluginsUpdated = 0
    indexNumberUpdated = 0
    print(oColors.brightBlack + f"Updating: {inputSelectedObject}" + oColors.standardWhite)
    print("┌─────┬────────────────────────────────┬────────────┬──────────┐")
    print("│ No. │ Name                           │ Old V.     │ New V.   │")
    print("└─────┴────────────────────────────────┴────────────┴──────────┘")
    try:
        for pluginArray in track(INSTALLEDPLUGINLIST, description="Updating" ,transient=True, complete_style="bright_magenta", ):
            plugin = INSTALLEDPLUGINLIST[i][0]
            if not configValues.localPluginFolder:
                pluginFile = f"{configValues.sftp_folderPath}/{plugin}"
                if configValues.sftp_useSftp:
                    pluginAttributes = sftp_validateFileAttributes(connection, pluginFile)
                    if pluginAttributes == False:
                        i += 1
                        continue
                else:
                    pluginAttributes = ftp_validateFileAttributes(connection, pluginFile)
                    if pluginAttributes == False:
                        i += 1
                        continue
            else:
                pluginFolderPath = configValues.pathToPluginFolder
                if not os.path.isfile(Path(f"{pluginFolderPath}/{plugin}")):
                    i += 1
                    continue
                if not re.search(r'.jar$', plugin):
                    i += 1
                    continue

            try:
                fileName = getFileName(plugin)
                fileVersion = getFileVersion(plugin)
                pluginId = INSTALLEDPLUGINLIST[i][1]
                latestVersion = INSTALLEDPLUGINLIST[i][3]
            except (TypeError, ValueError):
                i += 1
                continue

            if re.search(r'.jar$', fileName):
                fileName = eggCrackingJar(plugin, "name")

            pluginIdStr = str(pluginId)
            if pluginId == None or pluginId == '':
                i += 1
                continue

            if inputSelectedObject == 'all' or inputSelectedObject == pluginIdStr or re.search(inputSelectedObject, fileName, re.IGNORECASE):
                if INSTALLEDPLUGINLIST[i][4] == True:
                    print(f" [{indexNumberUpdated+1}]".rjust(6), end='')
                    print("  ", end='')
                    print(f"{fileName}".ljust(33), end='')
                    print(f"{fileVersion}".ljust(13), end='')
                    print(f"{latestVersion}".ljust(13))
                    if not configValues.localPluginFolder:
                        if configValues.sftp_seperateDownloadPath is True:
                            pluginPath = configValues.sftp_pathToSeperateDownloadPath
                        else:
                            pluginPath = configValues.sftp_folderPath
                        pluginPath = f"{pluginPath}/{plugin}"
                        indexNumberUpdated += 1
                        pluginsUpdated += 1
                        if configValues.sftp_useSftp:
                            sftp = createSFTPConnection()
                            try:
                                getSpecificPackage(pluginId, pluginPath)
                                if configValues.sftp_seperateDownloadPath is False:
                                    sftp.remove(pluginPath)
                            except HTTPError as err:
                                print(oColors.brightRed +  f"HTTPError: {err.code} - {err.reason}" + oColors.standardWhite)
                                pluginsUpdated -= 1
                            except FileNotFoundError:
                                print(oColors.brightRed +  f"FileNotFoundError: Old plugin file coulnd't be deleted" + oColors.standardWhite)

                        else:
                            ftp = createFTPConnection()
                            try:
                                getSpecificPackage(pluginId, pluginPath)
                                if configValues.sftp_seperateDownloadPath is False:
                                    ftp.delete(pluginPath)
                            except HTTPError as err:
                                print(oColors.brightRed +  f"HTTPError: {err.code} - {err.reason}" + oColors.standardWhite)
                                pluginsUpdated -= 1
                            except FileNotFoundError:
                                print(oColors.brightRed +  f"FileNotFoundError: Old plugin file coulnd't be deleted" + oColors.standardWhite)

                    else:
                        if configValues.seperateDownloadPath is True:
                            pluginPath = configValues.pathToSeperateDownloadPath
                        else:
                            pluginPath = configValues.pathToPluginFolder
                        indexNumberUpdated += 1
                        pluginsUpdated += 1
                        try:
                            getSpecificPackage(pluginId, pluginPath)
                            if configValues.seperateDownloadPath is False:
                                pluginPath = f"{pluginPath}/{plugin}"
                                os.remove(pluginPath)
                        except HTTPError as err:
                            print(oColors.brightRed +  f"HTTPError: {err.code} - {err.reason}" + oColors.standardWhite)
                            pluginsUpdated -= 1
                        except FileNotFoundError:
                            print(oColors.brightRed +  f"FileNotFoundError: Old plugin file coulnd't be deleted" + oColors.standardWhite)
                    if inputSelectedObject != 'all':
                        break
                elif inputSelectedObject != 'all':
                    print(oColors.brightGreen + f"{fileName} is already on {latestVersion}" + oColors.standardWhite)
                    print(oColors.brightRed + "Aborting the update process."+ oColors.standardWhite)
                    break
            else:
                i += 1
                continue

            i += 1
    except TypeError:
        print(oColors.brightRed + "Error occured: Aborted updating plugins." + oColors.standardWhite)
    except NameError:
        print(oColors.brightRed + "Check for updates before updating plugins with: 'check all'" + oColors.standardWhite)
        print(oColors.brightRed + "Started checking for updates..." + oColors.standardWhite)
        checkInstalledPackage()
        print(oColors.brightRed + f"Please input 'update {inputSelectedObject}' again!" + oColors.standardWhite)
    if i != 0:
        print(oColors.brightYellow + f"Plugins updated: [{pluginsUpdated}/{i}]" + oColors.standardWhite)
    if inputSelectedObject =='all' and pluginsUpdated == 0 and i != 0:
        print(oColors.brightGreen + "All found plugins are on the latest version!" + oColors.standardWhite)


def getInstalledPlugin(localFileName, localFileVersion, localPluginFullName):
    url = "https://api.spiget.org/v2/search/resources/" + localFileName + "?field=name&sort=-downloads"
    packageName = doAPIRequest(url)
    plugin_match_found = False
    pluginID = None
    localFileVersionNew = localFileVersion
    i = 0
    for i in range(0, 3):
        if plugin_match_found == True:
            break
        if i == 1:
            localFileVersionNew = re.sub(r'(\-\w*)', '', localFileVersion)
        if i == 2:
            pluginNameinYML = eggCrackingJar(localPluginFullName, 'name')
            url = "https://api.spiget.org/v2/search/resources/" + pluginNameinYML + "?field=name&sort=-downloads"
            try:
                packageName = doAPIRequest(url)
            except ValueError:
                continue

            localFileVersion = localFileVersionNew

        for resource in packageName:
            if plugin_match_found == True:
                continue
            pID = resource["id"]
            url2 = f"https://api.spiget.org/v2/resources/{pID}/versions?size=100&sort=-name"
            try:
                packageVersions = doAPIRequest(url2)
            except ValueError:
                continue
            for updates in packageVersions:
                updateVersion = updates["name"]
                if localFileVersionNew in updateVersion:
                    plugin_match_found = True
                    pluginID = pID
                    updateId = updates["id"]
                    plugin_latest_version = getLatestPluginVersion(pID)
                    plugin_is_outdated = compareVersions(plugin_latest_version, updateVersion)
                    addToPluginList(localPluginFullName, pID, updateId,  plugin_latest_version , plugin_is_outdated)
                    return pluginID

    else:
        if plugin_match_found != True:
            pID = updateId = plugin_latest_version = plugin_is_outdated = None
            addToPluginList(localPluginFullName, pID, updateId,  plugin_latest_version , plugin_is_outdated)

    return pluginID
