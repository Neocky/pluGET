import os
import sys
import configparser
from pathlib import Path

from utils.consoleoutput import oColors


class configurationValues:
    def __init__(self):
        config = configparser.ConfigParser()
        config.sections()
        config.read("config.ini")
        localPluginFolder = config['General']['UseLocalPluginFolder']
        self.pathToPluginFolder = Path(config['Local - This Machine']['PathToPluginFolder'])
        seperateDownloadPath = config['Local - This Machine']['SeperateDownloadPath']
        self.pathToSeperateDownloadPath = Path(config['Local - This Machine']['PathToSeperateDownloadPath'])

        self.sftp_server = config['SFTP - Remote Server']['Server']
        self.sftp_user = config['SFTP - Remote Server']['Username']
        self.sftp_password = config['SFTP - Remote Server']['Password']
        sftp_port = config['SFTP - Remote Server']['SFTPPort']
        self.sftp_folderPath = config['SFTP - Remote Server']['PluginFolderOnServer']
        sftp_useSftp = config['SFTP - Remote Server']['USE_SFTP']
        sftp_seperateDownloadPath = config['SFTP - Remote Server']['SeperateDownloadPath']
        self.sftp_pathToSeperateDownloadPath = config['SFTP - Remote Server']['PathToSeperateDownloadPath']

        self.sftp_port = int(sftp_port)
        if localPluginFolder == 'True':
            self.localPluginFolder = True
        else:
            self.localPluginFolder = False

        if seperateDownloadPath == 'True':
            self.seperateDownloadPath = True
        else:
            self.seperateDownloadPath = False

        if sftp_seperateDownloadPath == 'True':
            self.sftp_seperateDownloadPath = True
        else:
            self.sftp_seperateDownloadPath = False

        if sftp_useSftp == 'True':
            self.sftp_useSftp = True
        else:
            self.sftp_useSftp = False


def checkConfig():
    configAvailable = os.path.isfile("config.ini")
    if not configAvailable:
        createConfig()
        print(oColors.brightRed + "Config created. Edit config before executing again!" + oColors.standardWhite)
        input("Press any key + enter to exit...")
        sys.exit()


def createConfig():
    config = configparser.ConfigParser(allow_no_value=True)
    config['General'] = {}
    config['General'][';'] = 'If a local plugin folder exists (True/False) (If False SFTP/FTP will be used):'
    config['General']['UseLocalPluginFolder'] = 'True'

    config['Local - This Machine'] = {}
    config['Local - This Machine']['PathToPluginFolder'] = 'C:/Users/USER/Desktop/plugins'
    config['Local - This Machine'][';'] = 'For a different folder to store the updated plugins change to (True/False) and the path below'
    config['Local - This Machine']['SeperateDownloadPath'] = 'False'
    config['Local - This Machine']['PathToSeperateDownloadPath'] = 'C:/Users/USER/Desktop/plugins'

    config['SFTP - Remote Server'] = {}
    config['SFTP - Remote Server']['Server'] = '0.0.0.0'
    config['SFTP - Remote Server']['Username'] = 'user'
    config['SFTP - Remote Server']['Password'] = 'password'
    config['SFTP - Remote Server'][';'] = 'If a different Port for SFTP needs to be used (Works only for SFTP)'
    config['SFTP - Remote Server']['SFTPPort'] = '22'
    config['SFTP - Remote Server'][';_'] = 'Change the path below if the plugin folder path is different on the SFTP/FTP server (Change only if you know what you are doing)'
    config['SFTP - Remote Server']['PluginFolderOnServer'] = './plugins'
    config['SFTP - Remote Server'][';__'] = 'If you want to use FTP instead of SFTP change to (False) else use (True)'
    config['SFTP - Remote Server']['USE_SFTP'] = 'True'
    config['SFTP - Remote Server'][';___'] = 'For a different folder to store the updated plugins (Only with the update command!) change to (True/False) and the path below'
    config['SFTP - Remote Server']['SeperateDownloadPath'] = 'False'
    config['SFTP - Remote Server']['PathToSeperateDownloadPath'] = './plugins'


    with open('config.ini', 'w') as configfile:
        config.write(configfile)
