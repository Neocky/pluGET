import sys

from utils.consoleoutput import oColors
from utils.web_request import doAPIRequest
from handlers.handle_sftp import sftp_upload_file, sftp_cdPluginDir, createSFTPConnection

def getInstalledPaperMinecraftVersion(localPaperName):
    print("test")

def getInstalledPaperVersion(localPaperName):
    print("test")

# https://papermc.io/api/docs/swagger-ui/index.html?configUrl=/api/openapi/swagger-config#/
def papermc_downloader(paperBuild, paperVersionGroup='1.16'):
    url = f"https://papermc.io/api/v2/projects/paper/{serverVersion}/{inputPackageVersion}" # v1 is deprecated
    #https://papermc.io/api/v2/projects/paper/version_group/1.16/builds      get all builds for all 1.16 versions
    #https://papermc.io/api/v2/projects/paper/versions/1.16.5/builds/450     gets file name
    # input serverversion = 1.16.5 inputpackageversion = 450
    # regex 1.16 % build url
    # search for 450 in version group 1.16
    # if found get file name from builds/450
    # build url & download package
    # https://papermc.io/api/v2/projects/paper/versions/1.16.5/builds/450/downloads/paper-1.16.5-450.jar


    papermcdetails = doAPIRequest(url)
    errorExists = papermcdetails["error"]
    if errorExists in papermcdetails:
        print(f"PaperMc version: {inputPackageVersion} couldn't be found")
        print("Aborting the download of PaperMc.")
        input("Press any key + enter to exit...")
        sys.exit()
