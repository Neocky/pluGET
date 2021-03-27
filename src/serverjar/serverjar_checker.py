import os
import sys
from urllib.error import HTTPError
from pathlib import Path

from handlers.handle_sftp import createSFTPConnection, sftp_listFilesInServerRoot
from handlers.handle_config import configurationValues
from utils.consoleoutput import oColors
from serverjar.serverjar_paper import paperCheckForUpdate, papermc_downloader


def checkInstalledServerjar():
    configValues = configurationValues()
    if not configValues.localPluginFolder:
        sftp = createSFTPConnection()
        serverRootList = sftp_listFilesInServerRoot(sftp)
    else:
        serverRootList = os.path.dirname(configValues.pathToPluginFolder)
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
    print(oColors.brightBlack + f"Checking: {installedServerjarFullName}" + oColors.standardWhite)
    if 'paper' in installedServerjarFullName:
        paperCheckForUpdate(installedServerjarFullName)

    else:
        print(oColors.brightRed + f"{installedServerjarFullName} isn't supported.")
        print(oColors.brightRed + "Aborting the process." + oColors.standardWhite)


def updateServerjar(serverJarBuild='latest'):
    configValues = configurationValues()
    try:
        if serverJarBuild == None:
            serverJarBuild = 'latest'
        if not configValues.localPluginFolder:
            sftp = createSFTPConnection()
            serverRootPath = configValues.sftp_folderPath
            serverRootPath = Path(str(serverRootPath).replace(r'/plugins', ''))
            serverRootList = sftp_listFilesInServerRoot(sftp)

        else:
            serverRoot = os.path.dirname(configValues.pathToPluginFolder)
            serverRootList = os.listdir(serverRoot)
            serverRootPath = configValues.pathToPluginFolder
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
        print(oColors.brightBlack + f"Updating Paper to build: {serverJarBuild}" + oColors.standardWhite)
        if not configValues.localPluginFolder:
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
    