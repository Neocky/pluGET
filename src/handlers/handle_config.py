import os
import sys
import configparser

from utils.consoleoutput import oColors


def checkConfig():
    currentFolder = os.getcwd()
    os.chdir('..')
    configAvailable = os.path.isfile("config.ini")
    
    if not configAvailable:
        createConfig()
        print(oColors.brightRed + "Config created. Edit config before executing again!" + oColors.standardWhite)
        input("Press any key + enter to exit...")
        sys.exit()

    class configValues:
        config = configparser.ConfigParser()
        config.sections()
        config.read("config.ini")
        localPluginFolder = config['General']['LocalPluginFolder']
        pathToPluginFolder = config['General']['PathToPluginFolder']

        sftp_server = config['SFTP - Remote Server']['Server']
        sftp_user = config['SFTP - Remote Server']['Username']
        sftp_password = config['SFTP - Remote Server']['Password']
        sftp_port = config['SFTP - Remote Server']['Port']
        sftp_folderPath = config['SFTP - Remote Server']['PluginFolderForUpload']

        sftp_port = int(sftp_port)
        if localPluginFolder == 'True':
            localPluginFolder = True
        else:
            localPluginFolder = False
        
    os.chdir(currentFolder)
    return configValues


def createConfig():
    config = configparser.ConfigParser(allow_no_value=True)
    config['General'] = {}
    config['General'][';'] = 'If a local plugin folder exists (True/False): (If False SFTP will be used)'
    config['General']['LocalPluginFolder'] = 'True'
    config['General']['PathToPluginFolder'] = 'C:\\Users\\USER\\Desktop\\plugins'
    config['SFTP - Remote Server'] = {}
    config['SFTP - Remote Server']['Server'] = '0.0.0.0'
    config['SFTP - Remote Server']['Username'] = 'user'
    config['SFTP - Remote Server']['Password'] = 'password'
    config['SFTP - Remote Server'][';'] = 'Normally you won*t need to change anything below this line'
    config['SFTP - Remote Server']['Port'] = '22'
    config['SFTP - Remote Server']['PluginFolderForUpload'] = '.\\plugins'

    with open('./config.ini', 'w') as configfile:
        config.write(configfile)
