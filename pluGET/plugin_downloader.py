import urllib.request
import cgi
import time
import requests
import re
from consoleoutput import consoleTitle, clearConsole, printMainMenu
from plugin_updatechecker import getInstalledPackages


def calculateFileSize(downloadFileSize):
    fileSizeDownload = int(downloadFileSize)
    fileSizeMb = fileSizeDownload / 1024 / 1024
    roundedFileSize = round(fileSizeMb, 2)
    return roundedFileSize


def handleInput(inputString):
    if inputString == "1":
        downloadPackageManual()
    if inputString == "2":
        apiCallTest()
    if inputString == "3":
        searchPackage()
    if inputString == "4":
        getLatestPackageVersion()
    if inputString == "5":
        getInstalledPackages('C:\\Users\\Jan-Luca\\Desktop\\plugins')



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


# 28140 for Luckperms (Testing only)
def downloadPackageManual():
    ressourceId = input("SpigotMC Ressource ID: ")

    url = "https://api.spiget.org/v2/resources/" + ressourceId + "/download"
    #url2 = "https://api.spiget.org/v2/resources/" + ressourceId + "/versions/latest/download"
    #print(url2)
    #user_agent = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
    #header = { 'User-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11', 'Accept-Encoding': 'gzip, deflate, br' }
    #req = urllib.request.Request(url2, headers=header)
    #remotefile = urlopen(req)
    remotefile = urllib.request.urlopen(url)
    filecontent = remotefile.info()['Content-Disposition']
    filesize = remotefile.info()['Content-Length']
    # getting original filename
    value, params = cgi.parse_header(filecontent)
    filename = params["filename"]

    # creating file path
    path = r"C:\\Users\Jan-Luca\Desktop\\"
    ppath = path + filename

    # download file
    urllib.request.urlretrieve(url, ppath)

    filesizeData = calculateFileSize(filesize)
    print(f"Downloadsize: {filesizeData} MB")


# 89273
def handleRegexPackageName(packageNameFull):
    packageNameFull2 = packageNameFull
    # trims the part of the package that has for example "[1.1 Off]" in it
    unwantedpackageName = re.search(r'(^\[+[a-zA-Z0-9\s\W*\.*\-*\+*\%*\,]*\]+)', packageNameFull)
    unwantedpackageNamematch = bool(unwantedpackageName)
    if unwantedpackageNamematch:
        unwantedpackageNameString = unwantedpackageName.group()
        packageNameFull2 = packageNameFull.replace(unwantedpackageNameString, '')
        print(packageNameFull2)
        print("packageNameFull2")
    
    # gets the real packagename "word1 & word2" is not supported only gets word 1
    packageName = re.search(r'([a-zA-Z]\d*)+(\s?\-*\_*[a-zA-Z]\d*\+*\-*\'*)+', packageNameFull2)
    packageNameFullString = packageName.group()
    packageNameOnly = packageNameFullString.replace(' ', '')
    print(packageNameOnly)
    print("packageNameOnly")
    return packageNameOnly

def getlatestVersion(packageId):
    response = requests.get("https://api.spiget.org/v2/resources/" + packageId + "/versions/latest")
    #packageDetails = response.json()
    packageVersion = response.json()["name"]
    return packageVersion


def apiCallTest():
    ressourceId = input("SpigotMC Ressource ID: ")
    response = requests.get("https://api.spiget.org/v2/resources/" + ressourceId)
    packageDetails = response.json()
    print(packageDetails)
    packageName = response.json()["name"]
    packageTag = response.json()["tag"]
    print(packageName)
    print(packageTag)
    packageNameNew = handleRegexPackageName(packageName)
    print(packageNameNew)


# check version
def compareVersions():
    #https://api.spiget.org/v2/resources/28140/versions/latest
    # compare latest package version with installed package version
    print("compareVersions")


def searchPackage():
    ressourceName = input("    SpigotMC Ressource Name: ")
    response = requests.get("https://api.spiget.org/v2/search/resources/" + ressourceName + "?field=name")
    #https://api.spiget.org/v2/search/resources/luckperms?field=name
    print("https://api.spiget.org/v2/search/resources/" + ressourceName + "?field=name")
    packageName = response.json()
    i = 1
    for ressource in packageName:
        pName = ressource["name"]
        print(f"    [{i}] {pName}")
        i = i + 1

    ressourceSelected = int(input("    Select your wanted Ressource: "))
    ressourceSelected = ressourceSelected - 1
    fileInfo = response.json()[ressourceSelected]["file"]
    packageUrl = fileInfo["url"]
    ressourceId = response.json()[ressourceSelected]["id"]
    print(packageUrl)
    print(ressourceId)

def downloadLatestVersion(ressourceId, packageDownloadName, sourcePath):
    url = "https://api.spiget.org/v2/resources/" + ressourceId + "/download"
    remotefile = urllib.request.urlopen(url)
    filesize = remotefile.info()['Content-Length']
    downloadPath = sourcePath + packageDownloadName
    urllib.request.urlretrieve(url, downloadPath)
    filesizeData = calculateFileSize(filesize)
    print(f"    Downloadsize: {filesizeData} MB")


def getLatestPackageVersion():
    ressourceId = input("    SpigotMC Ressource ID: ")
    response = requests.get("https://api.spiget.org/v2/resources/" + ressourceId)
    packageDetails = response.json()
    packageName = response.json()["name"]
    packageTag = response.json()["tag"]
    packageNameNew = handleRegexPackageName(packageName)
    packageVersion = getlatestVersion(ressourceId)
    packageDownloadName = f"{packageNameNew}-{packageVersion}.jar"
    downloadPath = r"C:\\Users\Jan-Luca\Desktop\\"
    downloadLatestVersion(ressourceId, packageDownloadName, downloadPath)





consoleTitle()
inputMainMenu()
outputTest()


# get latest update > https://api.spiget.org/v2/resources/28140/updates/latest
# this also > https://api.spiget.org/v2/resources/28140/versions/latest
# get latest download with correct name > https://api.spiget.org/v2/resources/28140/versions/latest/download cloudflare protected
# query for a plugin https://api.spiget.org/v2/search/resources/luckperms?field=name
