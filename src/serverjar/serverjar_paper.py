import re
import urllib.request
from pathlib import Path
from rich.console import Console

from utils.consoleoutput import oColors
from utils.web_request import doAPIRequest
from handlers.handle_sftp import createSFTPConnection, sftp_upload_server_jar
from handlers.handle_ftp import createFTPConnection, ftp_upload_server_jar
from handlers.handle_config import configurationValues
from utils.utilities import createTempPluginFolder, deleteTempPluginFolder, calculateFileSizeMb


def getInstalledPaperMinecraftVersion(localPaperName):
    if localPaperName is None:
        return False
    mcVersionFull = re.search(r'(\d*\.*\d)+', localPaperName)
    try:
        mcVersion = mcVersionFull.group()
    except AttributeError:
        mcVersion = mcVersionFull
    return mcVersion


def getInstalledPaperVersion(localPaperName):
    if localPaperName is None:
        return False
    paperBuildFull = re.search(r'([\d]*.jar)', localPaperName)
    try:
        paperBuild = paperBuildFull.group()
    except AttributeError:
        paperBuild = paperBuildFull
    paperBuild = paperBuild.replace('.jar', '')
    return paperBuild


def findVersionGroup(mcVersion):
    versionGroups = ['1.17', '1.16', '1.15']
    if mcVersion is None:
        return False
    for versionGroup in versionGroups:
        url = f"https://papermc.io/api/v2/projects/paper/version_group/{versionGroup}/builds"
        papermcdetails = doAPIRequest(url)
        papermcVersionForMc = papermcdetails["versions"]
        for versions in papermcVersionForMc:
            if versions == mcVersion:
                paperVersionGroup = versionGroup
                return paperVersionGroup
            if versionGroup == mcVersion:
                paperVersionGroup = versionGroup
                return paperVersionGroup
    return False  # Not found


def findBuildVersion(wantedPaperBuild):
    versionGroups = ['1.17', '1.16', '1.15']
    if wantedPaperBuild is None:
        return False
    for versionGroup in versionGroups:
        url = f"https://papermc.io/api/v2/projects/paper/version_group/{versionGroup}/builds"
        papermcdetails = doAPIRequest(url)
        paperMcBuilds = papermcdetails["builds"]
        for build in paperMcBuilds:
            paperBuild = str(build["build"])
            if paperBuild == wantedPaperBuild:
                paperVersionGroup = build["version"]
                return paperVersionGroup
    return False  # Not found


def findLatestBuild(paperVersionGroup):
    if paperVersionGroup is None:
        return False
    url = f"https://papermc.io/api/v2/projects/paper/version_group/{paperVersionGroup}/builds"
    papermcbuilds = doAPIRequest(url)
    if "status" in papermcbuilds:  # Checks if the API returns a status. This means that there was an error.
        return False
    latestPaperBuild = papermcbuilds["builds"][-1]["build"]
    return latestPaperBuild


def findLatestBuildForVersion(mcVersion):
    if mcVersion is None:
        return False
    url = f"https://papermc.io/api/v2/projects/paper/versions/{mcVersion}"
    papermcbuilds = doAPIRequest(url)
    latestPaperBuild = papermcbuilds["builds"][-1]
    return latestPaperBuild


def versionBehind(installedPaperBuild, latestPaperBuild):
    if installedPaperBuild is None or latestPaperBuild is None:
        return False
    installedPaperBuildint = int(installedPaperBuild)
    latestPaperBuildint = int(latestPaperBuild)
    versionsBehind = latestPaperBuildint - installedPaperBuildint
    return versionsBehind


def getDownloadFileName(paperMcVersion, paperBuild):
    if paperMcVersion is None or paperBuild is None:
        return False
    url = f"https://papermc.io/api/v2/projects/paper/versions/{paperMcVersion}/builds/{paperBuild}"
    buildDetails = doAPIRequest(url)
    downloadName = buildDetails["downloads"]["application"]["name"]
    return downloadName


def paperCheckForUpdate(installedServerjarFullName):
    mcVersion = getInstalledPaperMinecraftVersion(installedServerjarFullName)

    # Report an error if getInstalledPaperMinecraftVersion encountered an issue.
    if not mcVersion:
        print(oColors.brightRed + f"ERR: An error was encountered while detecting the server's Minecraft version." +
              oColors.standardWhite)
        return False

    paperInstalledBuild = getInstalledPaperVersion(installedServerjarFullName)
    # Report an error if getInstalledPaperVersion encountered an issue.
    if not paperInstalledBuild:
        print(oColors.brightRed + f"ERR: An error was encountered while detecting the server's Paper version." +
              oColors.standardWhite)
        return False

    versionGroup = findVersionGroup(mcVersion)
    # Report an error if findVersionGroup encountered an issue.
    if not versionGroup:
        print(oColors.brightRed + f"ERR: An error was encountered while fetching the server's version group." +
              oColors.standardWhite)
        return False

    paperLatestBuild = findLatestBuild(versionGroup)
    # Report an error if findLatestBuild encountered an issue.
    if not paperLatestBuild:
        print(oColors.brightRed + f"ERR: An error was encountered while fetching the latest version of PaperMC." +
              oColors.standardWhite)
        return False  # Not currently handled, but can be at a later date. Currently just stops the following from
    #                   being printed.

    paperVersionBehind = versionBehind(paperInstalledBuild, paperLatestBuild)
    # Report an error if getInstalledPaperVersion encountered an issue.
    if not paperVersionBehind:
        print(oColors.brightRed + f"ERR: An error was encountered while detecting how many versions behind you are. "
                                  f"Will display as 'N/A'." + oColors.standardWhite)
        paperVersionBehind = "N/A"  # Sets paperVersionBehind to N/A while still letting the versionBehind check return
                                    # False for error-handing reasons.

        # Does not return false as versions behind doesn't break things. It is just helpful information.
        # paperVersionBehind will just display as "N/A"
    print("┌─────┬────────────────────────────────┬──────────────┬──────────────┬───────────────────┐")
    print("│ No. │ Name                           │ Installed V. │ Latest V.    │ Versions behind   │")
    print("└─────┴────────────────────────────────┴──────────────┴──────────────┴───────────────────┘")
    print("  [1]".rjust(6), end='')
    print("  ", end='')
    print("paper".ljust(33), end='')
    print(f"{paperInstalledBuild}".ljust(15), end='')
    print(f"{paperLatestBuild}".ljust(15), end='')
    print(f"{paperVersionBehind}".ljust(8))
    print(oColors.brightYellow + f"Versions behind: [{paperVersionBehind}]" + oColors.standardWhite)


# https://papermc.io/api/docs/swagger-ui/index.html?configUrl=/api/openapi/swagger-config#/
def papermc_downloader(paperBuild='latest', installedServerjarName=None, mcVersion=None):
    configValues = configurationValues()
    if configValues.localPluginFolder == False:
        downloadPath = createTempPluginFolder()
    else:
        downloadPath = configValues.pathToPluginFolder
        helpPath = Path('/plugins')
        helpPathstr = str(helpPath)
        downloadPath = Path(str(downloadPath).replace(helpPathstr, ''))

    if mcVersion == None:
        if paperBuild == 'latest':
            mcVersion = '1.17'
        else:
            mcVersion = findBuildVersion(paperBuild)

    if installedServerjarName != None:
        mcVersion = getInstalledPaperMinecraftVersion(installedServerjarName)

    if paperBuild == 'latest':
        paperBuild = findLatestBuildForVersion(mcVersion)
    try:
        downloadFileName = getDownloadFileName(mcVersion, paperBuild)
    except KeyError:
        print(oColors.brightRed + f"This version wasn't found for {mcVersion}" + oColors.standardWhite)
        print(oColors.brightRed + f"Reverting to latest version for {mcVersion}" + oColors.standardWhite)
        paperBuild = findLatestBuildForVersion(mcVersion)
        downloadFileName = getDownloadFileName(mcVersion, paperBuild)

    downloadPackagePath = Path(f"{downloadPath}/{downloadFileName}")
    if configValues.localPluginFolder == False:
        downloadPath = createTempPluginFolder()

    url = f"https://papermc.io/api/v2/projects/paper/versions/{mcVersion}/builds/{paperBuild}/downloads/{downloadFileName}"
    remotefile = urllib.request.urlopen(url)
    filesize = remotefile.info()['Content-Length']
    print(f"Getting Paper {paperBuild} for {mcVersion}")
    console = Console()
    with console.status("Downloading...", spinner='line', spinner_style='bright_magenta') as status:
        urllib.request.urlretrieve(url, downloadPackagePath)
    filesizeData = calculateFileSizeMb(filesize)
    print("Downloaded " + (str(filesizeData)).rjust(9) + f" MB here {downloadPackagePath}")
    if not configValues.localPluginFolder:
        if not configValues.sftp_useSftp:
            ftpSession = createFTPConnection()
            ftp_upload_server_jar(ftpSession, downloadPackagePath)
        else:
            sftpSession = createSFTPConnection()
            sftp_upload_server_jar(sftpSession, downloadPackagePath)

        deleteTempPluginFolder(downloadPath)

    print(oColors.brightGreen + "Downloaded successfully " + oColors.standardWhite + f"Paper {paperBuild}" + \
          oColors.brightGreen + " for " + oColors.standardWhite + f"{mcVersion}" + oColors.standardWhite)
