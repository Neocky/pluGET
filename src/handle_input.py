import time
from consoleoutput import consoleTitle, clearConsole, printMainMenu
from plugin_downloader import downloadPackageManual, apiCallTest, searchPackage, getLatestPackageVersionInteractive, getPackageVersion
from plugin_updatechecker import getInstalledPackages
from web_request import createCloudScraperInstance#, CLOUDSCRAPER



def handleInput(inputCommand, inputSelectedObject, inputParams="latest"):
    if inputCommand == 'get':
        getPackageVersion(inputSelectedObject, inputParams, r"C:\\Users\USER\Desktop\\")



def getInput():
    inputCommand, inputSelectedObject, *inputParams = input("pluGET >> ").split()
    inputParams = inputParams[0] if inputParams else ''
    print(inputCommand)
    print(inputSelectedObject)
    print(inputParams)
    handleInput(inputCommand, inputSelectedObject,inputParams)






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
        getLatestPackageVersionInteractive(r"C:\\Users\USER\Desktop\\")
    if inputString == "5":
        getInstalledPackages('C:\\Users\\USER\\Desktop\\plugins')


def inputMainMenu():
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


createCloudScraperInstance()
consoleTitle()
inputMainMenu()
outputTest()
