import sys

from utils.consoleoutput import oColors
from utils.utilities import getHelp
from handlers.handle_config import checkConfig
from plugin.plugin_downloader import searchPackage, getSpecificPackage
from plugin.plugin_updatechecker import updateInstalledPackage, checkInstalledPackage
from plugin.plugin_remover import removePlugin

def createInputLists():
    global COMMANDLIST
    COMMANDLIST = [
        'get',
        'update',
        'check',
        'search',
        'exit',
        'help',
        'remove'
    ]
    global INPUTSELECTEDOBJECT
    INPUTSELECTEDOBJECT = [
        'all',
        '*'
    ]


def handleInput(inputCommand, inputSelectedObject, inputParams):
    while True:
        if inputCommand == 'get':
            if inputSelectedObject.isdigit():
                if not checkConfig().localPluginFolder:
                    getSpecificPackage(inputSelectedObject, checkConfig().sftp_folderPath,  inputParams)
                    break
                else:
                    getSpecificPackage(inputSelectedObject, checkConfig().pathToPluginFolder,  inputParams)
                    break
            else:
                searchPackage(inputSelectedObject)
                break
        if inputCommand == 'update':
            updateInstalledPackage(inputSelectedObject)
            break
        if inputCommand == 'check':
            checkInstalledPackage(inputSelectedObject)
            break
        if inputCommand == 'search':
            searchPackage(inputSelectedObject)
            break
        if inputCommand == 'exit':
            sys.exit()
        if inputCommand == 'help':
            getHelp()
            break
        if inputCommand == 'remove':
            removePlugin(inputSelectedObject)
            break
        else:
            print(oColors.brightRed + "Command not found. Please try again." + oColors.standardWhite)
            getInput()
    getInput()


def getInput():
    while True:
        try:
            inputCommand, inputSelectedObject, *inputParams = input("pluGET >> ").split()
            break
        except ValueError:
            print(oColors.brightRed + "Wrong input! Use: > *command* *selectedObject* *optionalParams*" + oColors.standardWhite)

    inputParams = inputParams[0] if inputParams else None
    handleInput(inputCommand, inputSelectedObject, inputParams)
