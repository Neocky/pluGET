import sys
import pysftp
from handle_config import checkConfig
from consoleoutput import oColors

def createSFTPConnection():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None # TODO fix this
    sftp = pysftp.Connection(checkConfig().sftp_server, username=checkConfig().sftp_user, password=checkConfig().sftp_password, port=checkConfig().sftp_port, cnopts=cnopts)
    return sftp

def sftp_showPlugins(sftp):
    sftp.cd('plugins')
    for attr in sftp.listdir_attr():
        print(attr.filename, attr)

def sftp_cdPluginDir(sftp):
    sftp.cd('plugins')


def sftp_upload_file(sftp, itemPath):
    #sftp = createSFTPConnection()
    try:
        sftp.chdir('plugins')
        sftp.put(itemPath)

    except FileNotFoundError:
        print(oColors.brightRed + "The *plugins* folder couldn*t be found on the remote host!" + oColors.standardWhite)
        print(oColors.brightRed + "Aborting installation." + oColors.standardWhite)
    sftp.close()


def sftp_listAll(sftp):
    try:
        sftp.chdir('plugins')
        installedPlugins = sftp.listdir()

    except FileNotFoundError:
        print(oColors.brightRed + "The *plugins* folder couldn*t be found on the remote host!" + oColors.standardWhite)
    
    return installedPlugins