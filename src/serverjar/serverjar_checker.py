import os
import sys
from urllib.error import HTTPError
from pathlib import Path

from handlers.handle_sftp import createSFTPConnection, sftp_listFilesInServerRoot
from handlers.handle_config import checkConfig
from utils.consoleoutput import oColors
from serverjar.serverjar_paper import paperCheckForUpdate, papermc_downloader


def checkInstalledServerjar():
    if not checkConfig().localPluginFolder:
        sftp = createSFTPConnection()
        serverRootList = sftp_listFilesInServerRoot(sftp)
    else:
        serverRootList = os.path.dirname(checkConfig().pathToPluginFolder)
        serverRootList = os.listdir(serverRootList)
    installedServerjarFullName = None
    try:
        for files in serverRootList:
            try:
                if '.jar' in files:
                    installedServerjarFullName = files
                    break
            except TypeError:
                continue
    except TypeError:
        print(oColors.brightRed + "Serverjar couldn't be found." + oColors.standardWhite)
        print(oColors.brightRed + "Aborting the process." + oColors.standardWhite)

    if installedServerjarFullName == None:
        print(oColors.brightRed + "Serverjar couldn't be found." + oColors.standardWhite)
        print(oColors.brightRed + "Aborting the process." + oColors.standardWhite)
        input("Press any key + enter to exit...")
        sys.exit()

    if 'paper' in installedServerjarFullName:
        paperCheckForUpdate(installedServerjarFullName)

    else:
        print(oColors.brightRed + f"{installedServerjarFullName} isn't supported.")
        print(oColors.brightRed + "Aborting the process." + oColors.standardWhite)


def updateServerjar(serverJarBuild='latest'):
    try:
        if serverJarBuild == None:
            serverJarBuild = 'latest'
        if not checkConfig().localPluginFolder:
            sftp = createSFTPConnection()
            serverRootPath = checkConfig().sftp_folderPath
            serverRootPath = Path(str(serverRootPath).replace(r'/plugins', ''))
            serverRootList = sftp_listFilesInServerRoot(sftp)

        else:
            serverRoot = os.path.dirname(checkConfig().pathToPluginFolder)
            serverRootList = os.listdir(serverRoot)
            serverRootPath = checkConfig().pathToPluginFolder
            helpPath = Path('/plugins')
            helpPathstr = str(helpPath)
            serverRootPath = Path(str(serverRootPath).replace(helpPathstr, ''))
            installedServerjarFullName = None

    except FileNotFoundError:
        print(oColors.brightRed + "Path couldn't be found!" + oColors.standardWhite)
        print(oColors.brightRed + "Check your config!" + oColors.standardWhite)
        print(oColors.brightRed + "Aborting the process." + oColors.standardWhite)
        input("Press any key + enter to exit...")
        sys.exit()

    try:
        for files in serverRootList:
            try:
                if '.jar' in files:
                    installedServerjarFullName = files
                    break
            except TypeError:
                continue
    except TypeError:
        print(oColors.brightRed + "Serverjar couldn't be found." + oColors.standardWhite)
        print(oColors.brightRed + "Aborting the process." + oColors.standardWhite)

    if installedServerjarFullName == None:
        print(oColors.brightRed + "Serverjar couldn't be found." + oColors.standardWhite)
        print(oColors.brightRed + "Aborting the process." + oColors.standardWhite)
        input("Press any key + enter to exit...")
        sys.exit()

    serverJarPath = Path(f"{serverRootPath}/{installedServerjarFullName}")

    if 'paper' in installedServerjarFullName:
        print(f"Updating Paper to build: {serverJarBuild}")
        if not checkConfig().localPluginFolder:
            try:
                papermc_downloader(serverJarBuild, installedServerjarFullName)
                sftp.remove(serverJarPath)
            except HTTPError as err:
                print(oColors.brightRed +  f"Error: {err.code} - {err.reason}" + oColors.standardWhite)
            except FileNotFoundError:
                print(oColors.brightRed +  "Error: Old serverjar file coulnd't be deleted" + oColors.standardWhite)

        else:
            try:
                papermc_downloader(serverJarBuild, installedServerjarFullName)
                os.remove(serverJarPath)
            except HTTPError as err:
                print(oColors.brightRed +  f"Error: {err.code} - {err.reason}" + oColors.standardWhite)
            except FileNotFoundError:
                print(oColors.brightRed +  "Error: Old serverjar file coulnd't be deleted" + oColors.standardWhite)

    else:
        print(oColors.brightRed + f"{installedServerjarFullName} isn't supported.")
        print(oColors.brightRed + "Aborting the process." + oColors.standardWhite)
    