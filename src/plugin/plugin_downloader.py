import re
import urllib.request
from urllib.error import HTTPError
from pathlib import Path

from utils.consoleoutput import oColors
from utils.web_request import doAPIRequest
from utils.utilities import createTempPluginFolder, deleteTempPluginFolder, calculateFileSizeKb, calculateFileSizeMb
from handlers.handle_config import configurationValues
from handlers.handle_sftp import sftp_upload_file, sftp_cdPluginDir, createSFTPConnection


def handleRegexPackageName(packageNameFull):
    packageNameFull2 = packageNameFull
    # trims the part of the package that has for example "[1.1 Off]" in it
    unwantedpackageName = re.search(r'(^\[+[a-zA-Z0-9\s\W*\.*\-*\+*\%*\,]*\]+)', packageNameFull)
    unwantedpackageNamematch = bool(unwantedpackageName)
    if unwantedpackageNamematch:
        unwantedpackageNameString = unwantedpackageName.group()
        packageNameFull2 = packageNameFull.replace(unwantedpackageNameString, '')
    # gets the real packagename "word1 & word2" is not supported only gets word 1
    packageName = re.search(r'([a-zA-Z]\d*)+(\s?\-*\_*[a-zA-Z]\d*\+*\-*\'*)+', packageNameFull2)
    packageNameFullString = packageName.group()
    packageNameOnly = packageNameFullString.replace(' ', '')
    return packageNameOnly


def getVersionID(packageId, packageVersion):
    if packageVersion == None or packageVersion == 'latest':
        url = f"https://api.spiget.org/v2/resources/{packageId}/versions/latest"
        response = doAPIRequest(url)
        versionId = response["id"]
        return versionId

    url = f"https://api.spiget.org/v2/resources/{packageId}/versions?size=100&sort=-name"
    versionList = doAPIRequest(url)

    for packages in versionList:
        packageUpdate = packages["name"]
        versionId = packages["id"]
        if packageUpdate == packageVersion:
            return versionId
    return versionList[0]["id"]


def getVersionName(packageId, versionId):
    url = f"https://api.spiget.org/v2/resources/{packageId}/versions/{versionId}"
    response = doAPIRequest(url)
    versionName = response["name"]
    return versionName


def searchPackage(ressourceName):
    configValues = configurationValues()
    url = f"https://api.spiget.org/v2/search/resources/{ressourceName}?field=name&sort=-downloads"
    packageName = doAPIRequest(url)
    i = 1
    print(oColors.brightBlack + f"Searching: {ressourceName}" + oColors.standardWhite)
    print("┌─────┬─────────────────────────────┬───────────┬──────────────────────────────────────────────────────────────────────┐")
    print("│ No. │ Name                        │ Downloads │ Description                                                          │")
    print("└─────┴─────────────────────────────┴───────────┴──────────────────────────────────────────────────────────────────────┘")
    for ressource in packageName:
        pName = ressource["name"]
        newName = handleRegexPackageName(pName)
        pTag = ressource["tag"]
        pDownloads = ressource["downloads"]
        print(f" [{i}]".rjust(6), end='')
        print("  ", end='')
        print(f"{newName}".ljust(30), end='')
        print(f"{pDownloads}".rjust(9), end='')
        print("   ", end='')
        print(f"{pTag}".ljust(120))
        i = i + 1

    ressourceSelected = int(input("Select your wanted Ressource (No.)(0 to exit): "))
    if ressourceSelected != 0:
        ressourceSelected = ressourceSelected - 1
        ressourceId = packageName[ressourceSelected]["id"]
        if not configValues.localPluginFolder:
            try:
                getSpecificPackage(ressourceId, configValues.sftp_folderPath)
            except HTTPError as err:
                print(oColors.brightRed +  f"Error: {err.code} - {err.reason}" + oColors.standardWhite)
        else:
            try:
                getSpecificPackage(ressourceId, configValues.pathToPluginFolder)
            except HTTPError as err:
                print(oColors.brightRed +  f"Error: {err.code} - {err.reason}" + oColors.standardWhite)


def downloadSpecificVersion(ressourceId, downloadPath, versionID='latest'):
    configValues = configurationValues()
    if versionID != 'latest':
        #url = f"https://spigotmc.org/resources/{ressourceId}/download?version={versionID}"
        print(oColors.brightRed + "Sorry but specific version downloads aren't supported because of cloudflare protection. :(" + oColors.standardWhite)
        print(oColors.brightRed + "Reverting to latest version." + oColors.standardWhite)

    url = f"https://api.spiget.org/v2/resources/{ressourceId}/download"
    #url = f"https://api.spiget.org/v2/resources/{ressourceId}/versions/latest/download" #throws 403 forbidden error...cloudflare :(

    remotefile = urllib.request.urlopen(url)
    filesize = remotefile.info()['Content-Length']
    urllib.request.urlretrieve(url, downloadPath)
    filesize = int(filesize)
    print("        ", end='')
    if filesize >= 1000000:
        filesizeData = calculateFileSizeMb(filesize)
        print("Downloaded " + (str(filesizeData)).rjust(9) + f" MB here {downloadPath}")
    else:
        filesizeData = calculateFileSizeKb(filesize)
        print("Downloaded " + (str(filesizeData)).rjust(9) + f" KB here {downloadPath}")
    if not configValues.localPluginFolder:
        sftpSession = createSFTPConnection()
        sftp_upload_file(sftpSession, downloadPath)


def getSpecificPackage(ressourceId, downloadPath, inputPackageVersion='latest'):
    configValues = configurationValues()
    if configValues.localPluginFolder == False:
        downloadPath = createTempPluginFolder()
    url = f"https://api.spiget.org/v2/resources/{ressourceId}"
    packageDetails = doAPIRequest(url)
    packageName = packageDetails["name"]
    packageNameNew = handleRegexPackageName(packageName)
    versionId = getVersionID(ressourceId, inputPackageVersion)
    packageVersion = getVersionName(ressourceId, versionId)
    packageDownloadName = f"{packageNameNew}-{packageVersion}.jar"
    downloadPackagePath = Path(f"{downloadPath}/{packageDownloadName}")
    if configValues.localPluginFolder:
        if inputPackageVersion is None or inputPackageVersion == 'latest':
            downloadSpecificVersion(ressourceId=ressourceId, downloadPath=downloadPackagePath)
        else:
            downloadSpecificVersion(ressourceId, downloadPackagePath, versionId)

    if not configValues.localPluginFolder:
        if inputPackageVersion is None or inputPackageVersion == 'latest':
            downloadSpecificVersion(ressourceId=ressourceId, downloadPath=downloadPackagePath)
            deleteTempPluginFolder(downloadPath)
        else:
            downloadSpecificVersion(ressourceId, downloadPackagePath, versionId)
            deleteTempPluginFolder(downloadPath)
