import os
import sys
import re
import urllib.request

from utils.consoleoutput import oColors
from utils.web_request import doAPIRequest
from handlers.handle_sftp import sftp_upload_server_jar, sftp_cdPluginDir, createSFTPConnection
from handlers.handle_config import checkConfig
from utils.utilities import createTempPluginFolder, deleteTempPluginFolder
from plugin.plugin_downloader import calculateFileSize



# = 1.16.5
def getInstalledPaperMinecraftVersion(localPaperName):
    mcVersionFull = re.search(r'(\d*\.*\d)+', localPaperName)
    try:
        mcVersion = mcVersionFull.group()
    except AttributeError:
        mcVersion = mcVersionFull
    return mcVersion


# = 550
def getInstalledPaperVersion(localPaperName):
    paperBuildFull = re.search(r'([\d]*.jar)', localPaperName)
    try:
        paperBuild = paperBuildFull.group()
    except AttributeError:
        paperBuild = paperBuildFull
    paperBuild = paperBuild.replace('.jar', '')
    return paperBuild


def findVersionGroup(mcVersion):
    versionGroups = ['1.16', '1.15']
    versionGroupFound = False
    for versionGroup in versionGroups:
        if versionGroupFound == True:
            break
        url = f"https://papermc.io/api/v2/projects/paper/version_group/{versionGroup}/builds"
        papermcdetails = doAPIRequest(url)
        papermcVersionForMc = papermcdetails["versions"]
        for versions in papermcVersionForMc:
            if versions == mcVersion:
                versionGroupFound = True
                paperVersionGroup = versionGroup
                break
            if versionGroup == mcVersion:
                versionGroupFound = True
                paperVersionGroup = versionGroup
                print(versionGroup)
                break

    return paperVersionGroup


def findLatestBuild(paperVersionGroup):
    url = f"https://papermc.io/api/v2/projects/paper/version_group/{paperVersionGroup}/builds"
    papermcbuilds = doAPIRequest(url)
    latestPaperBuild = papermcbuilds["builds"][-1]["build"]
    return latestPaperBuild


def versionBehind(installedPaperBuild, latestPaperBuild):
    installedPaperBuildint = int(installedPaperBuild)
    latestPaperBuildint = int(latestPaperBuild)
    versionsBehind = latestPaperBuildint - installedPaperBuildint
    return versionsBehind



def getDownloadFileName(paperMcVersion, paperBuild):
    url = f"https://papermc.io/api/v2/projects/paper/versions/{paperMcVersion}/builds/{paperBuild}"
    buildDetails = doAPIRequest(url)
    downloadName = buildDetails["downloads"]["application"]["name"]
    return downloadName


def paperCheckForUpdate(installedServerjarFullName):
    mcVersion = getInstalledPaperMinecraftVersion(installedServerjarFullName)
    paperInstalledBuild = getInstalledPaperVersion(installedServerjarFullName)
    versionGroup = findVersionGroup(mcVersion)
    paperLatestBuild = findLatestBuild(versionGroup)
    paperVersionBehind = versionBehind(paperInstalledBuild, paperLatestBuild)

    print(f"Paper for {mcVersion}")
    print("Index | Name               |   Old V.   |   New V.   | Versions behind ")
    print(f" [1]".ljust(8), end='')
    print(f"paper".ljust(24), end='')
    print(f"{paperInstalledBuild}".ljust(8), end='')
    print("     ", end='')
    print(f"{paperLatestBuild}".ljust(8), end='')
    print("     ", end='')
    print(f"{paperVersionBehind}".ljust(8))


# https://papermc.io/api/docs/swagger-ui/index.html?configUrl=/api/openapi/swagger-config#/
def papermc_downloader(paperBuild='latest', installedServerjarName=None, mcVersion=None):
    if checkConfig().localPluginFolder == False:
        downloadPath = createTempPluginFolder()
    else:
        downloadPath = checkConfig().pathToPluginFolder
        downloadPath = downloadPath.replace(r'\plugins', '')

    if mcVersion == None:
        mcVersion = '1.16.5'
    
    if installedServerjarName != None:
        mcVersion = getInstalledPaperMinecraftVersion(installedServerjarName)

    if paperBuild == 'latest':
        versionGroup = findVersionGroup(mcVersion)
        paperBuild = findLatestBuild(versionGroup)
    try:
        downloadFileName = getDownloadFileName(mcVersion, paperBuild)
    except KeyError:
        print(oColors.brightRed + f"This version wasn't found for {mcVersion}" + oColors.standardWhite)
        print(oColors.brightRed + f"Reverting to latest version for {mcVersion}" + oColors.standardWhite)
        versionGroup = findVersionGroup(mcVersion)
        paperBuild = findLatestBuild(versionGroup)
        downloadFileName = getDownloadFileName(mcVersion, paperBuild)

    downloadPackagePath = f"{downloadPath}\\{downloadFileName}"

    if checkConfig().localPluginFolder == False:
        downloadPath = createTempPluginFolder()

    url = f"https://papermc.io/api/v2/projects/paper/versions/{mcVersion}/builds/{paperBuild}/downloads/{downloadFileName}"
    remotefile = urllib.request.urlopen(url)
    filesize = remotefile.info()['Content-Length']
    print(f"Starting paper-{paperBuild} download for {mcVersion}...")
    urllib.request.urlretrieve(url, downloadPackagePath)
    filesizeData = calculateFileSize(filesize)

    print(f"Downloadsize: {filesizeData} KB")
    print(f"File downloaded here: {downloadPackagePath}")
    if not checkConfig().localPluginFolder:
        sftpSession = createSFTPConnection()
        sftp_upload_server_jar(sftpSession, downloadPackagePath)
        deleteTempPluginFolder(downloadPath)
