import os
import sys
import ftplib
import stat
import re

from utils.consoleoutput import oColors
from handlers.handle_config import configurationValues


def createFTPConnection():
    configValues = configurationValues()
    try:
        ftp = ftplib.FTP()
        ftp.connect(configValues.sftp_server, configValues.ftp_port)
        ftp.login(configValues.sftp_user, configValues.sftp_password)
        return ftp
    except UnboundLocalError:
        print(oColors.brightRed + "[FTP]: Check your config.ini!" + oColors.standardWhite)
        print(oColors.brightRed + "Exiting program..." + oColors.standardWhite)
        sys.exit()


def ftp_showPlugins(ftp):
    configValues = configurationValues()
    ftp.cwd(configValues.sftp_folderPath)
    for attr in ftp.dir():
        print(attr.filename, attr)


def ftp_upload_file(ftp, itemPath):
    configValues = configurationValues()
    if configValues.sftp_seperateDownloadPath is True:
        uploadFolderPath = configValues.sftp_pathToSeperateDownloadPath
    else:
        uploadFolderPath = configValues.sftp_folderPath
    try:
        ftp.cwd(uploadFolderPath)
        itemPath = os.path.relpath(itemPath, 'TempSFTPFolder/')
        itemPath = str(itemPath)
        currentDirectory = os.getcwd()
        os.chdir('TempSFTPFolder')
        with open (itemPath, 'rb') as plugin_file:
            ftp.storbinary('STOR '+ str(itemPath), plugin_file)
    except FileNotFoundError:
        print(oColors.brightRed + "[FTP]: The 'plugins' folder couldn*t be found on the remote host!" + oColors.standardWhite)
        print(oColors.brightRed + "[FTP]: Aborting uploading." + oColors.standardWhite)
    os.chdir(currentDirectory)
    ftp.close()


def ftp_upload_server_jar(ftp, itemPath):
    try:
        ftp.cwd('.')
        itemPath = os.path.relpath(itemPath, 'TempSFTPFolder/')
        itemPath = str(itemPath)
        currentDirectory = os.getcwd()
        os.chdir('TempSFTPFolder')
        with open (itemPath, 'rb') as server_jar:
            ftp.storbinary('STOR '+ str(itemPath), server_jar)
    except FileNotFoundError:
        print(oColors.brightRed + "[FTP]: The 'root' folder couldn*t be found on the remote host!" + oColors.standardWhite)
        print(oColors.brightRed + "[FTP]: Aborting uploading." + oColors.standardWhite)
    os.chdir(currentDirectory)
    ftp.close()


def ftp_listAll(ftp):
    configValues = configurationValues()
    try:
        ftp.cwd(configValues.sftp_folderPath)
        installedPlugins = ftp.nlst()
    except FileNotFoundError:
        print(oColors.brightRed + "[FTP]: The 'plugins' folder couldn*t be found on the remote host!" + oColors.standardWhite)

    try:
        return installedPlugins
    except UnboundLocalError:
        print(oColors.brightRed + "[FTP]: No plugins were found." + oColors.standardWhite)


def ftp_listFilesInServerRoot(ftp):
    try:
        ftp.cwd('.')
        filesInServerRoot = ftp.nlst()
    except FileNotFoundError:
        print(oColors.brightRed + "[FTP]: The 'root' folder couldn*t be found on the remote host!" + oColors.standardWhite)

    try:
        return filesInServerRoot
    except UnboundLocalError:
        print(oColors.brightRed + "[FTP]: No Serverjar was found." + oColors.standardWhite)


def ftp_downloadFile(ftp, downloadPath, fileToDownload):
    configValues = configurationValues()
    ftp.cwd(configValues.sftp_folderPath)
    filedata = open(downloadPath,'wb')
    ftp.retrbinary('RETR '+fileToDownload, filedata.write)
    filedata.close()
    ftp.quit()


def ftp_is_file(ftp, pluginPath):
    if ftp.nlst(pluginPath) == [pluginPath]:
        return True
    else:
        return False


def ftp_validateFileAttributes(ftp, pluginPath):
    if ftp_is_file(ftp, pluginPath) is False:
        return False
    if re.search(r'.jar$', pluginPath):
        return True
    else:
        return False
