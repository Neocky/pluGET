import time
from consoleoutput import consoleTitle, clearConsole, printMainMenu
from plugin_downloader import downloadPackageManual, apiCallTest, searchPackage, getLatestPackageVersionInteractive
from plugin_updatechecker import getInstalledPackages


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


def handleInput(inputString):
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
    inputSt = input("    pluGET >> ")
    handleInput(inputSt)


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
