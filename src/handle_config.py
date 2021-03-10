# handles the config and everything around it
import sys
import configparser
import os.path

from consoleoutput import oColors


def checkConfig():
    configAvailable = os.path.isfile("./config.ini")
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

        sftp_server = config['Remote Server']['Server']
        sftp_user = config['Remote Server']['Username']
        sftp_password = config['Remote Server']['Password']
        sftp_port = config['Remote Server']['Port']
        sftp_folderPath = config['Remote Server']['PluginFolder']

        sftp_port = int(sftp_port)
        if localPluginFolder == 'True':
            localPluginFolder = True
        else:
            localPluginFolder = False
        
    return configValues


def createConfig():
    config = configparser.ConfigParser(allow_no_value=True)
    config['General'] = {}
    config['General'][';'] = 'If a local plugin folder exists (True/False): (If false use sftp)'
    config['General']['LocalPluginFolder'] = 'True'
    config['General']['PathToPluginFolder'] = 'C:\\Users\\USER\\Desktop\\plugins'
    config['Remote Server'] = {}
    config['Remote Server']['Server'] = '0.0.0.0'
    config['Remote Server']['Username'] = 'user'
    config['Remote Server']['Password'] = 'longpassword'
    config['Remote Server']['Port'] = '22'
    config['Remote Server']['PluginFolder'] = '.\\plugins'

    with open('./config.ini', 'w') as configfile:
        config.write(configfile)
