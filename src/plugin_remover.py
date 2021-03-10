import os
import re
from handle_config import checkConfig
from handle_sftp import createSFTPConnection, sftp_listAll

def removePlugin(pluginToRemove):
    if not checkConfig().localPluginFolder:
        sftp = createSFTPConnection()
        pluginList = sftp_listAll(sftp)
    else:
        pluginList = os.listdir(checkConfig().pathToPluginFolder)

    for plugin in pluginList:
        #pluginVersion = re.search(pluginToRemove, pluginNameFull)
        print(plugin)