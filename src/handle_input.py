import time
import sys
from consoleoutput import consoleTitle, clearConsole, printMainMenu, oColors
from plugin_downloader import searchPackage, getSpecificPackage
from plugin_updatechecker import updateInstalledPackage, checkInstalledPackage
from handle_config import checkConfig
from utilities import getHelp, check_requirements
from handle_sftp import createSFTPConnection, sftp_showPlugins
from plugin_remover import removePlugin

def createInputLists():
    global COMMANDLIST
    COMMANDLIST = [
        'get',
        'update',
        'check',
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
            else:
                searchPackage(inputSelectedObject)
                break
        if inputCommand == 'update':
            updateInstalledPackage(inputSelectedObject)
            break
        if inputCommand == 'check':
            checkInstalledPackage(inputSelectedObject)
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
    print(inputCommand)
    print(inputSelectedObject)
    print(inputParams)
    handleInput(inputCommand, inputSelectedObject, inputParams)


def inputMainMenu():
    consoleTitle()
    clearConsole()
    checkConfig()
    check_requirements()
    createInputLists()
    printMainMenu()
    getInput()
    outputTest()


def outputTest():
    print("Hello world")
    print("Waiting still seconds: 5", end='\r')
    time.sleep(1)
    print("Waiting still seconds: 4", end='\r')
    time.sleep(1)
    print("Waiting still seconds: 3", end='\r')
    time.sleep(1)
    print("Waiting still seconds: 2", end='\r')
    time.sleep(1)
    print("Waiting still seconds: 1", end='\r')
    time.sleep(1)
    print("Done ✅☑✔                ")
    input("Press key to end program...")


inputMainMenu()
