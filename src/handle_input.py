import time
import sys
from consoleoutput import consoleTitle, clearConsole, printMainMenu, oColors
from plugin_downloader import searchPackage, getSpecificPackage
from plugin_updatechecker import updateInstalledPackage, checkInstalledPackage
from handle_config import checkConfig
from utilities import getHelp

def createInputLists():
    global COMMANDLIST
    COMMANDLIST = [
        'get',
        'update',
        'check',
        'exit',
        'help'
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
                getSpecificPackage(inputSelectedObject, checkConfig().pathToPluginFolder,  inputParams)
                break
            else:
                searchPackage(inputSelectedObject)
                break
        if inputCommand == 'update':
            updateInstalledPackage(checkConfig().pathToPluginFolder, inputSelectedObject)
            break
        if inputCommand == 'check':
            checkInstalledPackage(checkConfig().pathToPluginFolder, inputSelectedObject)
            break
        if inputCommand == 'exit':
            sys.exit()
        if inputCommand == 'help':
            getHelp()
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
    clearConsole()
    checkConfig()
    createInputLists()
    printMainMenu()
    getInput()


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


consoleTitle()
inputMainMenu()
outputTest()
