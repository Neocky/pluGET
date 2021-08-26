import re
import urllib.request
from urllib.error import HTTPError
from pathlib import Path

from utils.consoleoutput import oColors
from utils.web_request import doAPIRequest
from utils.utilities import createTempPluginFolder, deleteTempPluginFolder, calculateFileSizeKb, calculateFileSizeMb
from handlers.handle_config import configurationValues
from handlers.handle_sftp import sftp_upload_file, createSFTPConnection
from handlers.handle_ftp import ftp_upload_file, createFTPConnection


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
    try:
        packageNameFullString = packageName.group()
        packageNameOnly = packageNameFullString.replace(' ', '')
    except AttributeError:
        packageNameOnly = unwantedpackageNameString
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


def searchPackage(resourceName):
    configValues = configurationValues()
    url = f"https://api.spiget.org/v2/search/resources/{resourceName}?field=name&sort=-downloads"
    packageName = doAPIRequest(url)
    i = 1
    print(oColors.brightBlack + f"Searching: {resourceName}" + oColors.standardWhite)
    print("┌─────┬─────────────────────────────┬───────────┬──────────────────────────────────────────────────────────────────────┐")
    print("│ No. │ Name                        │ Downloads │ Description                                                          │")
    print("└─────┴─────────────────────────────┴───────────┴──────────────────────────────────────────────────────────────────────┘")
    for resource in packageName:
        pName = resource["name"]
        newName = handleRegexPackageName(pName)
        pTag = resource["tag"]
        pDownloads = resource["downloads"]
        print(f" [{i}]".rjust(6), end='')
        print("  ", end='')
        print(f"{newName}".ljust(30), end='')
        print(f"{pDownloads}".rjust(9), end='')
        print("   ", end='')
        print(f"{pTag}".ljust(120))
        i = i + 1

    resourceSelected = int(input("Select your wanted resource (No.)(0 to exit): "))
    if resourceSelected != 0:
        resourceSelected = resourceSelected - 1
        resourceId = packageName[resourceSelected]["id"]
        if not configValues.localPluginFolder:
            if configValues.sftp_seperateDownloadPath is True:
                pluginDownloadPath = configValues.sftp_pathToSeperateDownloadPath
            else:
                pluginDownloadPath = configValues.sftp_folderPath
        else:
            if configValues.seperateDownloadPath is True:
                pluginDownloadPath = configValues.pathToSeperateDownloadPath
            else:
                pluginDownloadPath = configValues.pathToPluginFolder
        try:
            getSpecificPackage(resourceId, pluginDownloadPath)
        except HTTPError as err:
            print(oColors.brightRed +  f"Error: {err.code} - {err.reason}" + oColors.standardWhite)


def downloadSpecificVersion(resourceId, downloadPath, versionID='latest'):
    configValues = configurationValues()
    if versionID != 'latest':
        #url = f"https://spigotmc.org/resources/{resourceId}/download?version={versionID}"
        print(oColors.brightRed + "Sorry but specific version downloads aren't supported because of cloudflare protection. :(" + oColors.standardWhite)
        print(oColors.brightRed + "Reverting to latest version." + oColors.standardWhite)

    url = f"https://api.spiget.org/v2/resources/{resourceId}/download"
    #url = f"https://api.spiget.org/v2/resources/{resourceId}/versions/latest/download" #throws 403 forbidden error...cloudflare :(

    urrlib_opener = urllib.request.build_opener()
    urrlib_opener.addheaders = [('User-agent', 'pluGET/1.0')]
    urllib.request.install_opener(urrlib_opener)

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
        if configValues.sftp_useSftp:
            sftpSession = createSFTPConnection()
            sftp_upload_file(sftpSession, downloadPath)
        else:
            ftpSession = createFTPConnection()
            ftp_upload_file(ftpSession, downloadPath)


def getSpecificPackage(resourceId, downloadPath, inputPackageVersion='latest'):
    configValues = configurationValues()
    if configValues.localPluginFolder == False:
        downloadPath = createTempPluginFolder()
    url = f"https://api.spiget.org/v2/resources/{resourceId}"
    packageDetails = doAPIRequest(url)
    try:
        packageName = packageDetails["name"]
    except KeyError:
        print(oColors.brightRed +  "Error: Plugin ID couldn't be found" + oColors.standardWhite)
        return None
    packageNameNew = handleRegexPackageName(packageName)
    versionId = getVersionID(resourceId, inputPackageVersion)
    packageVersion = getVersionName(resourceId, versionId)
    packageDownloadName = f"{packageNameNew}-{packageVersion}.jar"
    downloadPackagePath = Path(f"{downloadPath}/{packageDownloadName}")
    if inputPackageVersion is None or inputPackageVersion == 'latest':
        downloadSpecificVersion(resourceId=resourceId, downloadPath=downloadPackagePath)
    else:
        downloadSpecificVersion(resourceId, downloadPackagePath, versionId)

    if not configValues.localPluginFolder:
        deleteTempPluginFolder(downloadPath)
