import time
from consoleoutput import consoleTitle, clearConsole, printMainMenu
from plugin_downloader import downloadPackageManual, apiCallTest, searchPackage, getLatestPackageVersion
from plugin_updatechecker import getInstalledPackages


def handleInput(inputString):
    if inputString == "1":
        downloadPackageManual()
    if inputString == "2":
        apiCallTest()
    if inputString == "3":
        searchPackage()
    if inputString == "4":
        ressourceID = inputOption(inputString)
        getLatestPackageVersion(ressourceID, r"C:\\Users\USER\Desktop\\")
    if inputString == "5":
        getInstalledPackages('C:\\Users\\USER\\Desktop\\plugins')


def inputMainMenu():
    clearConsole()
    printMainMenu()
    inputSt = input("    pluGET >> ") 
    handleInput(inputSt)


def inputOption(inputOption):
    if inputOption == "1":
        ressourceID = input("SpigotMC Ressource ID: ")
        return ressourceID


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