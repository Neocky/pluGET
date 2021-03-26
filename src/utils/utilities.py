# misc functions
import os
import sys
import shutil
import requests
from pathlib import Path

from utils.consoleoutput import oColors
from handlers.handle_config import checkConfig, configurationValues
from handlers.handle_sftp import createSFTPConnection


def getHelp():
    print(oColors.brightYellow+ "Need help?" + oColors.standardWhite)
    print("For a list of all commands: 'help command'")
    print("Or check the docs here:")
    print("https://github.com/Neocky/pluGET")
    print("Or go to the official discord.")
    print("The link for discord can also be found on Github!")


def getCommandHelp(optionalParams):
    if optionalParams == None:
        optionalParams = 'all'
    print(oColors.brightBlack + f"Help for command: {optionalParams}" +oColors.standardWhite)
    print("┌────────────────┬─────────────────┬─────────────────┬────────────────────────────────────────────────────────┐")
    print("│ Command        │ Selected Object │ Optional Params │ Function                                               │")
    print("└────────────────┴─────────────────┴─────────────────┴────────────────────────────────────────────────────────┘")
    while True:
        if optionalParams == 'all':
            print(oColors.brightBlack + " GENERAL:" + oColors.standardWhite)
            print("  exit             ./anything                          Exit pluGET")
            print("  help             ./anything                          Get general help")
            print("  help             command           all/command       Get specific help to the commands of pluGET")
            print(oColors.brightBlack + " PLUGIN MANAGEMENT:" + oColors.standardWhite)
            print("  get              Name/ID           Version           Downloads the latest version of a plugin")
            print("  check            Name/ID/all                         Check for an update of an installed plugin")
            print("  update           Name/ID/all                         Update installed plugins to the latest version")
            print("  search           Name                                Search for a plugin and download the latest version")
            print("  remove           Name/ID                             Delete an installed plugin")
            print(oColors.brightBlack + " SERVER SOFTWARE MANAGEMENT:" + oColors.standardWhite)
            print("  check            serverjar                           Check installed server software for an update")
            print("  update           serverjar         Version/Latest    Update installed server software to a specific version")
            print("  get-paper        PaperVersion      McVersion         Downloads a specific PaperMc version")
            break

        if optionalParams == 'exit':
            print(oColors.brightBlack + " GENERAL:" + oColors.standardWhite)
            print("  exit             ./anything                          Exit pluGET")
            break

        if optionalParams == 'help':
            print(oColors.brightBlack + " GENERAL:" + oColors.standardWhite)
            print("  help             ./anything                          Get general help")
            print("  help             command           all/command       Get specific help to the commands of pluGET")
            break

        if optionalParams == 'get':
            print(oColors.brightBlack + " PLUGIN MANAGEMENT:" + oColors.standardWhite)
            print(print("  get              Name/ID           Version           Downloads the latest version of a plugin"))
            break

        if optionalParams == 'check':
            print(oColors.brightBlack + " PLUGIN MANAGEMENT:" + oColors.standardWhite)
            print("  check            Name/ID/all                         Check for an update of an installed plugin")
            print(oColors.brightBlack + " SERVER SOFTWARE MANAGEMENT:" + oColors.standardWhite)
            print("  check            serverjar                           Check installed server software for an update")
            break

        if optionalParams == 'update':
            print(oColors.brightBlack + " PLUGIN MANAGEMENT:" + oColors.standardWhite)
            print("  update           Name/ID/all                         Update installed plugins to the latest version")
            print(oColors.brightBlack + " SERVER SOFTWARE MANAGEMENT:" + oColors.standardWhite)
            print("  update           serverjar         Version/Latest    Update installed server software to a specific version")
            break

        if optionalParams == 'search':
            print(oColors.brightBlack + " PLUGIN MANAGEMENT:" + oColors.standardWhite)
            print("  search           Name                                Search for a plugin and download the latest version")
            break

        if optionalParams == 'remove':
            print(oColors.brightBlack + " PLUGIN MANAGEMENT:" + oColors.standardWhite)
            print("  remove           Name/ID                             Delete an installed plugin")
            break

        if optionalParams == 'get-paper':
            print(oColors.brightBlack + " SERVER SOFTWARE MANAGEMENT:" + oColors.standardWhite)
            print("  get-paper        PaperVersion      McVersion         Downloads a specific PaperMc version")
            break

        else:
            print(oColors.brightRed + "Error: Help for Command not found. Please try again. :(" + oColors.standardWhite)
            break


def check_local_plugin_folder():
    if checkConfig().localPluginFolder:
        if checkConfig().seperateDownloadPath:
            pluginFolderPath = checkConfig().pathToSeperateDownloadPath
        else:
            pluginFolderPath = checkConfig().pathToPluginFolder

        if not os.path.isdir(pluginFolderPath):
            print(oColors.brightRed + "Plugin folder coulnd*t be found. Creating one..." + oColors.standardWhite)
            try:
                os.mkdir(pluginFolderPath)
            except OSError:
                print(oColors.brightRed + "Creation of directory %s failed" % pluginFolderPath)
                print(oColors.brightRed + "Please check the config file!" + oColors.standardWhite)
                input("Press any key + enter to exit...")
                sys.exit()
            else:
                print("Created directory %s" % pluginFolderPath)


def apiTest():
    apiStatusUrl = 'https://api.spiget.org/v2/status'
    try:
        r = requests.get(apiStatusUrl)
    except requests.exceptions.HTTPError:
        print(oColors.brightRed + "Couldn't make a connection to the API. Check you connection to the internet!" + oColors.standardWhite)
        input("Press any key + enter to exit...")
        sys.exit()
    if r.status_code != 200:
        print(oColors.brightRed + "Problems with the API detected. Plese try it again later!" + oColors.standardWhite)
        input("Press any key + enter to exit...")
        sys.exit()


def check_requirements():
    apiTest()
    check_local_plugin_folder()
    if not checkConfig().localPluginFolder:
        createSFTPConnection()


def createTempPluginFolder():
    tempPluginFolder = Path("./TempSFTPUploadFolder")
    if not os.path.isdir(tempPluginFolder):
        try:
            os.mkdir(tempPluginFolder)
        except OSError:
            print(oColors.brightRed + "Creation of directory %s failed" % checkConfig().pathToPluginFolder)
            print(oColors.brightRed + "Please check the config file!" + oColors.standardWhite)
            input("Press any key + enter to exit...")
            sys.exit()
    return tempPluginFolder


def deleteTempPluginFolder(tempPluginFolder):
    try:
        shutil.rmtree(tempPluginFolder)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))


def calculateFileSizeMb(downloadFileSize):
    fileSizeDownload = int(downloadFileSize)
    fileSizeMb = fileSizeDownload / 1024 / 1024
    roundedFileSize = round(fileSizeMb, 2)
    return roundedFileSize

def calculateFileSizeKb(downloadFileSize):
    fileSizeDownload = int(downloadFileSize)
    fileSizeKb = fileSizeDownload / 1024
    roundedFileSize = round(fileSizeKb, 2)
    return roundedFileSize