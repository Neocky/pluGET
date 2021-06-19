import sys
import os
import pysftp
import paramiko
import stat
import re

from utils.consoleoutput import oColors
from handlers.handle_config import configurationValues


def createSFTPConnection():
    configValues = configurationValues()
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None # TODO fix this
    try:
        sftp = pysftp.Connection(configValues.sftp_server, username=configValues.sftp_user, \
               password=configValues.sftp_password, port=configValues.sftp_port, cnopts=cnopts)
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
    configValues = configurationValues()
    sftp.cd(configValues.sftp_folderPath)
    for attr in sftp.listdir_attr():
        print(attr.filename, attr)


def sftp_upload_file(sftp, itemPath):
    configValues = configurationValues()
    try:
        sftp.chdir(configValues.sftp_folderPath)
        sftp.put(itemPath)

    except FileNotFoundError:
        print(oColors.brightRed + "[SFTP]: The 'plugins' folder couldn*t be found on the remote host!" + oColors.standardWhite)
        print(oColors.brightRed + "[SFTP]: Aborting uploading." + oColors.standardWhite)
    sftp.close()


def sftp_upload_server_jar(sftp, itemPath):
    try:
        sftp.chdir('.')
        sftp.put(itemPath)
    except FileNotFoundError:
        print(oColors.brightRed + "[SFTP]: The 'root' folder couldn*t be found on the remote host!" + oColors.standardWhite)
        print(oColors.brightRed + "[SFTP]: Aborting uploading." + oColors.standardWhite)
    sftp.close()


def sftp_listAll(sftp):
    configValues = configurationValues()
    try:
        sftp.chdir(configValues.sftp_folderPath)
        installedPlugins = sftp.listdir()
    except FileNotFoundError:
        print(oColors.brightRed + "[SFTP]: The 'plugins' folder couldn*t be found on the remote host!" + oColors.standardWhite)

    try:
        return installedPlugins
    except UnboundLocalError:
        print(oColors.brightRed + "[SFTP]: No plugins were found." + oColors.standardWhite)


def sftp_listFilesInServerRoot(sftp):
    try:
        filesInServerRoot = sftp.listdir()
    except FileNotFoundError:
        print(oColors.brightRed + "[SFTP]: The 'root' folder couldn*t be found on the remote host!" + oColors.standardWhite)

    try:
        return filesInServerRoot
    except UnboundLocalError:
        print(oColors.brightRed + "[SFTP]: No Serverjar was found." + oColors.standardWhite)


def sftp_downloadFile(sftp, downloadPath, fileToDownload):
    configValues = configurationValues()
    sftp.cwd(configValues.sftp_folderPath)
    currentDirectory = os.getcwd()
    os.chdir('TempSFTPFolder')
    sftp.get(fileToDownload)
    sftp.close()
    os.chdir(currentDirectory)


def sftp_validateFileAttributes(sftp, pluginPath):
    pluginSFTPAttribute = sftp.lstat(pluginPath)
    if stat.S_ISDIR(pluginSFTPAttribute.st_mode):
        return False
    elif re.search(r'.jar$', pluginPath):
        return True
    else:
        return False
