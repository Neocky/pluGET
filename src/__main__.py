from utils.consoleoutput import consoleTitle, clearConsole, printMainMenu, oColors
from utils.utilities import getHelp, check_requirements
from handlers.handle_input import createInputLists, getInput
from handlers.handle_config import checkConfig
from plugin.plugin_downloader import searchPackage, getSpecificPackage
from plugin.plugin_updatechecker import updateInstalledPackage, checkInstalledPackage
from plugin.plugin_remover import removePlugin


def mainFunction():
    consoleTitle()
    clearConsole()
    checkConfig()
    check_requirements()
    createInputLists()
    printMainMenu()
    getInput()

mainFunction()
