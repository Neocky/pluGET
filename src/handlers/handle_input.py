import sys

from utils.consoleoutput import oColors
from utils.utilities import getHelp, getCommandHelp
from handlers.handle_config import configurationValues
from plugin.plugin_downloader import searchPackage, getSpecificPackage
from plugin.plugin_updatechecker import updateInstalledPackage, checkInstalledPackage
from plugin.plugin_remover import removePlugin
from serverjar.serverjar_checker import checkInstalledServerjar, updateServerjar
from serverjar.serverjar_paper import papermc_downloader


def createInputLists():
    global COMMANDLIST
    COMMANDLIST = [
        'get',
        'update',
        'check',
        'search',
        'exit',
        'help',
        'remove',
        'get-paper'
    ]
    global INPUTSELECTEDOBJECT
    INPUTSELECTEDOBJECT = [
        'all',
        '*'
    ]


def handleInput(inputCommand, inputSelectedObject, inputParams):
    configValues = configurationValues()
    while True:
        if inputCommand == 'get':
            if inputSelectedObject.isdigit():
                if not configValues.localPluginFolder:
                    if configValues.sftp_seperateDownloadPath is True:
                        pluginPath = configValues.sftp_pathToSeperateDownloadPath
                    else:
                        pluginPath = configValues.sftp_folderPath
                    getSpecificPackage(inputSelectedObject, pluginPath,  inputParams)
                    break
                else:
                    if configValues.seperateDownloadPath is True:
                        pluginPath = configValues.pathToSeperateDownloadPath
                    else:
                        pluginPath = configValues.pathToPluginFolder
                    getSpecificPackage(inputSelectedObject, pluginPath,  inputParams)
                    break
            else:
                searchPackage(inputSelectedObject)
                break
        if inputCommand == 'update':
            if inputSelectedObject == 'serverjar':
                updateServerjar(inputParams)
            else:
                updateInstalledPackage(inputSelectedObject)
            break
        if inputCommand == 'check':
            if inputSelectedObject == 'serverjar':
                checkInstalledServerjar()
            else:
                checkInstalledPackage(inputSelectedObject, inputParams)
            break
        if inputCommand == 'search':
            searchPackage(inputSelectedObject)
            break
        if inputCommand == 'exit':
            sys.exit()
        if inputCommand == 'help':
            if inputSelectedObject == 'command' or inputSelectedObject == 'commands':
                getCommandHelp(inputParams)
            else:
                getHelp()
            break
        if inputCommand == 'remove':
            removePlugin(inputSelectedObject)
            break
        if inputCommand == 'get-paper':
            papermc_downloader(inputSelectedObject, inputParams)
            break
        else:
            print(oColors.brightRed + "Error: Command not found. Please try again. :(" + oColors.standardWhite)
            print(oColors.brightRed + "Use: '" + oColors.standardWhite +"help command" + oColors.brightRed +"' to get all available commands" + oColors.standardWhite)
            getInput()
    getInput()


def getInput():
    inputCommand = None
    while True:
        try:
            inputCommand, inputSelectedObject, *inputParams = input("pluGET >> ").split()
            break
        except ValueError:
            if inputCommand == None:
                continue
            else:
                print(oColors.brightRed + "Wrong input! Use: > 'command' 'selectedObject' [optionalParams]" + oColors.standardWhite)
                print(oColors.brightRed + "Use: '" + oColors.standardWhite +"help command" + oColors.brightRed +"' to get all available commands" + oColors.standardWhite)
        except KeyboardInterrupt:
            sys.exit()
    inputParams = inputParams[0] if inputParams else None
    handleInput(inputCommand, inputSelectedObject, inputParams)
