import sys
import pysftp
import paramiko

from utils.consoleoutput import oColors
from handlers.handle_config import checkConfig


def createSFTPConnection():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None # TODO fix this
    try:
        sftp = pysftp.Connection(checkConfig().sftp_server, username=checkConfig().sftp_user, \
               password=checkConfig().sftp_password, port=checkConfig().sftp_port, cnopts=cnopts)
    except paramiko.ssh_exception.AuthenticationException:
        print(oColors.brightRed + "[SFTP]: Wrong Username/Password" + oColors.standardWhite)
    except paramiko.ssh_exception.SSHException:
        print(oColors.brightRed + "[SFTP]: The SFTP server isn't available." + oColors.standardWhite)
    try:
        return sftp
    except UnboundLocalError:
        print(oColors.brightRed + "[SFTP]: Check your config.ini!" + oColors.standardWhite)
        print(oColors.brightRed + "Exiting program..." + oColors.standardWhite)
        sys.exit()


def sftp_showPlugins(sftp):
    sftp.cd('plugins')
    for attr in sftp.listdir_attr():
        print(attr.filename, attr)


def sftp_cdPluginDir(sftp):
    sftp.cd('plugins')


def sftp_upload_file(sftp, itemPath):
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

    try:
        return installedPlugins
    except UnboundLocalError:
        print(oColors.brightRed + "No plugins were found." + oColors.standardWhite)