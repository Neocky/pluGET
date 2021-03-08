import time
import sys
from consoleoutput import consoleTitle, clearConsole, printMainMenu, oColors
from plugin_downloader import downloadPackageManual, apiCallTest, searchPackage, getPackageVersion
from plugin_updatechecker import updateInstalledPackage, checkInstalledPackage


def createInputLists():
    global COMMANDLIST
    COMMANDLIST = [
        'get',
        'update',
        'check',
        'exit'
    ]
    global INPUTSELECTEDOBJECT
    INPUTSELECTEDOBJECT = [
        'all',
        '*'
    ]


def handleInput(inputCommand, inputSelectedObject, inputParams):
    while True:
        if inputCommand == 'get':
            getPackageVersion(r"C:\\Users\USER\Desktop\\", inputSelectedObject, inputParams)
            break
        if inputCommand == 'update':
            #if inputSelectedObject in INPUTSELECTEDOBJECT:
            updateInstalledPackage(r'C:\\Users\\USER\\Desktop\\plugins', inputSelectedObject)
            break
        if inputCommand == 'check':
            checkInstalledPackage(r'C:\\Users\\USER\\Desktop\\plugins', inputSelectedObject)
            break
        if inputCommand == 'exit':
            sys.exit()
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


def inputOption(inputOptionString):
    inputString = None
    print(inputOptionString)
    if inputOptionString == 1:
        inputString = input("SpigotMC Ressource ID: ")
    if inputOptionString == 2:
        inputString = input("SpigotMC Ressource ID: ")
    if inputOptionString == 3:
        inputString = input("    SpigotMC Ressource Name: ")
        print("ich bin ein test")
    return inputString


def handleInputOLD(inputString):
    if inputString == "1":
        downloadPackageManual()
    if inputString == "2":
        ressourceId = inputOption(2)
        apiCallTest(ressourceId)
    if inputString == "3":
        ressourceName = inputOption(3)
        searchPackage(ressourceName)
    if inputString == "4":
        #getLatestPackageVersionInteractive(r"C:\\Users\USER\Desktop\\")
        print("4")
    if inputString == "5":
        #updateAllInstalledPackages(r'C:\\Users\\USER\\Desktop\\plugins')
        print("5")


def inputMainMenu():
    createInputLists()
    clearConsole()
    printMainMenu()
    getInput()
    #inputSt = input("    pluGET >> ")
    #handleInputOLD(inputSt)


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


#createCloudScraperInstance()
consoleTitle()
inputMainMenu()
outputTest()
