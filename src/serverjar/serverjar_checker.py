import os
import sys
from urllib.error import HTTPError

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
        os.chdir('..')
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
    if serverJarBuild == None:
        serverJarBuild = 'latest'
    if not checkConfig().localPluginFolder:
        sftp = createSFTPConnection()
        serverRootList = sftp_listFilesInServerRoot(sftp)
    else:
        serverRoot = os.path.dirname(checkConfig().pathToPluginFolder)
        os.chdir('..')
        serverRootList = os.listdir(serverRoot)
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
        print(serverJarBuild)
        try:
            papermc_downloader(serverJarBuild, installedServerjarFullName)
        except HTTPError as err:
                print(oColors.brightRed +  f"Error: {err.code} - {err.reason}" + oColors.standardWhite)

    else:
        print(oColors.brightRed + f"{installedServerjarFullName} isn't supported.")
        print(oColors.brightRed + "Aborting the process." + oColors.standardWhite)
    