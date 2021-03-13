from os import system
from os import name


def consoleTitle():
    system("title " + "pluGET │ By Neocky")


def clearConsole():
    system('cls' if name=='nt' else 'clear')


# https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences
class oColors:
    standardWhite = "\033[0m"
    brightYellow = "\033[93m"
    brightMagenta = "\033[95m"
    brightRed = "\033[91m"
    brightGreen = "\033[92m"
    darkMagenta = "\033[35m"


def printLogo():
    print()
    print(oColors.brightYellow + r"          ___           ___       ___           ___           ___           ___     ")
    print(oColors.brightMagenta + r"         /\  " + oColors.brightYellow + r"\         " + oColors.brightMagenta + r"/"'\\' +
    oColors.brightYellow + r"__\     " + oColors.brightMagenta + r"/"'\\' + oColors.brightYellow + r"__\         " +
    oColors.brightMagenta + r"/\  "+ oColors.brightYellow + r"\         " + oColors.brightMagenta + r"/\  "+
    oColors.brightYellow + r"\         " + oColors.brightMagenta + r"/\  "+ oColors.brightYellow + r""'\\    ')
    print(oColors.brightMagenta + r"        /::\  "+ oColors.brightYellow + r"\       " + oColors.brightMagenta + r"/:/  " +
    oColors.brightYellow + r"/    " + oColors.brightMagenta + r"/:/  "+ oColors.brightYellow + r"/        " +
    oColors.brightMagenta + r"/::\  "+ oColors.brightYellow + r"\       " + oColors.brightMagenta + r"/::\  "+
    oColors.brightYellow + r"\        " + oColors.brightMagenta + r"\:\  "+ oColors.brightYellow + r""'\\   ')
    print(oColors.brightMagenta + r"       /:/\:\  "+ oColors.brightYellow + r"\     " + oColors.brightMagenta + r"/:/  "+
    oColors.brightYellow + r"/    " + oColors.brightMagenta + r"/:/  "+ oColors.brightYellow + r"/        " +
    oColors.brightMagenta + r"/:/\:\  "+ oColors.brightYellow + r"\     " + oColors.brightMagenta + r"/:/\:\  "+
    oColors.brightYellow + r"\        " + oColors.brightMagenta + r"\:\  "+ oColors.brightYellow + r""'\\  ')
    print(oColors.brightMagenta + r"      /::"'\\' + oColors.brightYellow + r"~" + oColors.brightMagenta + r"\:\  "+
    oColors.brightYellow + r"\   " + oColors.brightMagenta + r"/:/  "+ oColors.brightYellow + r"/    " +
    oColors.brightMagenta + r"/:/  "+ oColors.brightYellow + r"/  ___   " + oColors.brightMagenta + r"/:/  \:\  "+
    oColors.brightYellow + r"\   " + oColors.brightMagenta + r"/::"'\\'+ oColors.brightYellow + r"~" +
    oColors.brightMagenta + r"\:\  "+ oColors.brightYellow + r"\       " + oColors.brightMagenta + r"/::\  "+
    oColors.brightYellow + r""'\\')
    print(oColors.brightMagenta + r"     /:/\:\ \:"'\\'+ oColors.brightYellow + r"__\ " + oColors.brightMagenta + r"/:/"+
    oColors.brightYellow + r"__/    " + oColors.brightMagenta + r"/:/"+ oColors.brightYellow + r"__/  " +
    oColors.brightMagenta + r"/"'\\'+ oColors.brightYellow + r"__\ " + oColors.brightMagenta + r"/:/"+
    oColors.brightYellow + r"__/_" + oColors.brightMagenta + r"\:"'\\'+ oColors.brightYellow + r"__\ " +
    oColors.brightMagenta + r"/:/\:\ \:"'\\' + oColors.brightYellow + r"__\     " +
    oColors.brightMagenta + r"/:/\:"'\\'+ oColors.brightYellow + r"__\ ")
    print(oColors.brightMagenta + r"     " + oColors.brightMagenta + r"\/"+ oColors.brightYellow + r"__" +
    oColors.brightMagenta + r"\:\/:/"+ oColors.brightYellow + r"  / " + oColors.brightMagenta + r"\:"'\\'+
    oColors.brightYellow + r"  \    " + oColors.brightMagenta + r"\:"'\\' + oColors.brightYellow + r"  \ " +
    oColors.brightMagenta + r"/:/  "+ oColors.brightYellow + r"/ " + oColors.brightMagenta + r"\:\  /\ \/" +
    oColors.brightYellow + r"__/ " + oColors.brightMagenta + r"\:"'\\' + oColors.brightYellow + r"~" +
    oColors.brightMagenta + r"\:\ \/" + oColors.brightYellow + r"__/    " + oColors.brightMagenta + r"/:/  \/"+
    oColors.brightYellow + r"__/")
    print(oColors.brightMagenta + r"          \::/  "+ oColors.brightYellow + r"/   " + oColors.brightMagenta + r"\:\  "+
    oColors.brightYellow + r"\    " + oColors.brightMagenta + r"\:\  /:/  "+ oColors.brightYellow + r"/   " +
    oColors.brightMagenta + r"\:\ \:"'\\'+ oColors.brightYellow + r"__\    " + oColors.brightMagenta + r"\:\ \:"'\\'+
    oColors.brightYellow + r"__\     " + oColors.brightMagenta + r"/:/  "+ oColors.brightYellow + r"/     ")
    print(oColors.brightMagenta + r"           \/"+ oColors.brightYellow + r"__/     " +
    oColors.brightMagenta + r"\:\  " + oColors.brightYellow + r"\    " + oColors.brightMagenta + r"\:\/:/  "+
    oColors.brightYellow + r"/     " + oColors.brightMagenta + r"\:\/:/  "+ oColors.brightYellow + r"/     " +
    oColors.brightMagenta + r"\:\ \/"+ oColors.brightYellow + r"__/     " + oColors.brightMagenta + r"\/"+
    oColors.brightYellow + r"__/      ")
    print(oColors.brightMagenta + r"                      \:"'\\' + oColors.brightYellow + r"__\    " +
    oColors.brightMagenta + r"\::/  " + oColors.brightYellow + r"/       " + oColors.brightMagenta + r"\::/  " +
    oColors.brightYellow + r"/       " + oColors.brightMagenta + r"\:"'\\' + oColors.brightYellow + r"__\                  ")
    print(oColors.brightMagenta + r"                       \/" + oColors.brightYellow + r"__/     " +
    oColors.brightMagenta + r"\/" + oColors.brightYellow + r"__/         " + oColors.brightMagenta + r"\/" +
    oColors.brightYellow + r"__/         " + oColors.brightMagenta + r"\/" + oColors.brightYellow + r"__/                  " +
    oColors.standardWhite)
    print()
    print()
    print(oColors.brightYellow + "                                      [" + oColors.darkMagenta + "By Neocky" +
    oColors.brightYellow + "]                                    " + oColors.standardWhite)
    print()


def printHorizontalLine():
    print("    ─────────────────────────────────────────────────────────────────────────────────")


def printMainMenu():
    printLogo()
    printHorizontalLine()
