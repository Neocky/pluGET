# misc functions
import os
import sys
import shutil
import requests

from utils.consoleoutput import oColors
from handlers.handle_config import checkConfig


def getHelp():
    print(oColors.brightYellow+ "Need help?" + oColors.standardWhite)
    print("Check the docs here:")
    print("https://github.com/Neocky/pluGET")
    print("Or go to the official discord.")
    print("The link for discord can also be found on Github!")


def check_local_plugin_folder():
    if checkConfig().localPluginFolder:
        if not os.path.isdir(checkConfig().pathToPluginFolder):
            print(oColors.brightRed + "Plugin folder coulnd*t be found. Creating one..." + oColors.standardWhite)
            try:
                os.mkdir(checkConfig().pathToPluginFolder)
            except OSError:
                print(oColors.brightRed + "Creation of directory %s failed" % checkConfig().pathToPluginFolder)
                print(oColors.brightRed + "Please check the config file!" + oColors.standardWhite)
                sys.exit()
            else:
                print("Created directory %s" % checkConfig().pathToPluginFolder)


def apiTest():
    apiStatusUrl = 'https://api.spiget.org/v2/status'
    try:
        r = requests.get(apiStatusUrl)
    except requests.exceptions.HTTPError:
        print(oColors.brightRed + "Couldn't make a connection to the API. Check you connection to the internet!" + oColors.standardWhite)
        sys.exit()
    if r.status_code != 200:
        print(oColors.brightRed + "Problems with the API detected. Plese try it again later!" + oColors.standardWhite)
        sys.exit()


def check_requirements():
    apiTest()
    check_local_plugin_folder()
    # sftp test

def createTempPluginFolder():
    tempPluginFolder = ".\\plugins"
    if not os.path.isdir(tempPluginFolder):
        #print(oColors.brightRed + "Plugin folder coulnd*t be found. Creating one..." + oColors.standardWhite)
        try:
            os.mkdir(tempPluginFolder)
        except OSError:
            print(oColors.brightRed + "Creation of directory %s failed" % checkConfig().pathToPluginFolder)
            print(oColors.brightRed + "Please check the config file!" + oColors.standardWhite)
            sys.exit()
    return tempPluginFolder


def deleteTempPluginFolder(tempPluginFolder):
    try:
        shutil.rmtree(tempPluginFolder)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
