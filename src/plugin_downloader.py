import urllib.request
import cgi
import re
from web_request import doAPIRequest


def calculateFileSize(downloadFileSize):
    fileSizeDownload = int(downloadFileSize)
    fileSizeKb = fileSizeDownload / 1024
    roundedFileSize = round(fileSizeKb, 2)
    return roundedFileSize


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
    #print(packageNameOnly)
    #print("packageNameOnly")
    return packageNameOnly


def getlatestVersion(packageId):
    url = f"https://api.spiget.org/v2/resources/{packageId}/versions/latest"
    response = doAPIRequest(url)
    packageVersion = response["name"]
    return packageVersion


def apiCallTest(ressourceId):
    url = f"https://api.spiget.org/v2/resources/{ressourceId}"
    response = doAPIRequest(url)
    print(response)
    packageName = response["name"]
    packageTag = response["tag"]
    print(packageName)
    print(packageTag)
    packageNameNew = handleRegexPackageName(packageName)
    print(packageNameNew)


def getVersionID(packageId, packageVersion):
    print(packageVersion)
    if packageVersion == None or packageVersion == 'latest':
        url = f"https://api.spiget.org/v2/resources/{packageId}/versions/latest"
        response = doAPIRequest(url)
        versionId = response["id"]
        return versionId

    url = f"https://api.spiget.org/v2/resources/{packageId}/versions?size=100&sort=-name"
    versionList = doAPIRequest(url)

    for packages in versionList:
        packageUpdate = packages["name"]
        versionId = packages["id"]
        if packageUpdate == packageVersion:
            return versionId
    return versionList[0]["id"]


def getVersionName(packageId, versionId):
    url = f"https://api.spiget.org/v2/resources/{packageId}/versions/{versionId}"
    response = doAPIRequest(url)
    versionName = response["name"]
    return versionName


def searchPackage(ressourceName):
    url = f"https://api.spiget.org/v2/search/resources/{ressourceName}?field=name"
    packageName = doAPIRequest(url)
    print(url)
    i = 1
    print("Index  /  Name  /  Description  /  Downloads")
    for ressource in packageName:
        pName = ressource["name"]
        pTag = ressource["tag"]
        pDownloads = ressource["downloads"]
        print(f"    [{i}] {pName} / {pTag}/ {pDownloads}")
        i = i + 1

    ressourceSelected = int(input("    Select your wanted Ressource: "))
    ressourceSelected = ressourceSelected - 1
    fileInfo = packageName[ressourceSelected]["file"]
    packageUrl = fileInfo["url"]
    ressourceId = packageName[ressourceSelected]["id"]
    print(packageUrl)
    print(ressourceId)


def downloadSpecificVersion(ressourceId, downloadPath, versionID='latest'):
    print(versionID)
    if versionID != 'latest':
        #url = f"https://spigotmc.org/resources/{ressourceId}/download?version={versionID}"
        print("Sorry but specific version downloads aren't supported because of cloudflare protection. :(")

    url = f"https://api.spiget.org/v2/resources/{ressourceId}/download"
    #url = f"https://api.spiget.org/v2/resources/{ressourceId}/versions/latest/download" #throws 403 forbidden error

    remotefile = urllib.request.urlopen(url)
    filesize = remotefile.info()['Content-Length']
    urllib.request.urlretrieve(url, downloadPath)
    filesizeData = calculateFileSize(filesize)
    print(f"File downloaded here: {downloadPath}")
    print(f"Downloadsize: {filesizeData} KB")


def getPackageVersion(ressourceId, downloadPath, inputPackageVersion='latest'):
    url = f"https://api.spiget.org/v2/resources/{ressourceId}"
    packageDetails = doAPIRequest(url)
    packageName = packageDetails["name"]
    #packageTag = packageDetails["tag"]
    packageNameNew = handleRegexPackageName(packageName)
    versionId = getVersionID(ressourceId, inputPackageVersion)
    packageVersion = getVersionName(ressourceId, versionId)
    #packageVersion = getlatestVersion(ressourceId)
    packageDownloadName = f"{packageNameNew}-{packageVersion}.jar"
    downloadPackagePath = downloadPath + packageDownloadName

    if inputPackageVersion is None or inputPackageVersion == 'latest':
        downloadSpecificVersion(ressourceId=ressourceId, downloadPath=downloadPackagePath)
    else:
        downloadSpecificVersion(ressourceId, downloadPackagePath, versionId)

# get latest update > https://api.spiget.org/v2/resources/28140/updates/latest
# this also > https://api.spiget.org/v2/resources/28140/versions/latest
# get latest download with correct name > https://api.spiget.org/v2/resources/28140/versions/latest/download cloudflare protected
# query for a plugin https://api.spiget.org/v2/search/resources/luckperms?field=name
