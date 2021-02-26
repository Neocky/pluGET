import urllib.request
from urllib.request import urlopen
from urllib.request import urlretrieve
import cgi
from consoleoutput import consoleTitle, clearConsole, printMainMenu
import time


def calculateFileSize(downloadFileSize):
    fileSizeDownload = int(downloadFileSize)
    fileSizeMb = fileSizeDownload / 1024 / 1024
    roundedFileSize = round(fileSizeMb, 2)
    return roundedFileSize

consoleTitle()

print("if you see this clearConsole dont work")
clearConsole()
printMainMenu()
choice = input("pluGET >> ")
if choice == "1":
    ressourceId = input("SpigotMC Ressource ID: ")

# 28140 for Luckperms (Testing only)
url = "https://api.spiget.org/v2/resources/" + ressourceId + "/download"
print(url)

# getting original filename
remotefile = urlopen(url)
filecontent = remotefile.info()['Content-Disposition']
filesize = remotefile.info()['Content-Length']
value, params = cgi.parse_header(filecontent)
filename = params["filename"]

# creating file path
path = r"C:\\Users\USERNAME\Desktop\\"
ppath = path + filename

# download file
urllib.request.urlretrieve(url, ppath)

filesizeData = calculateFileSize(filesize) 
print(filesizeData)

#print(format(filesizeinmb, '.2f'))

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
print("Done ✅")
input("Taste drücken zum Beenden...")