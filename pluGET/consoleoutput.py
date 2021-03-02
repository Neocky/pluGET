# Handles the console output
from os import system
from os import name

def consoleTitle():
    system("title " + "🧱 pluGET │ by Neocky")


def clearConsole():
    system('cls' if name=='nt' else 'clear')


class oColors:
    standardWhite = "\033[0m"
    brightYellow = "\033[93m"
    brightMagenta = "\033[95m"
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
    print(oColors.brightYellow + "                                      [" + oColors.darkMagenta + "by Neocky" +
    oColors.brightYellow + "]                                    " + oColors.standardWhite)
    print()


def printMainMenu():
    printLogo()
    print("    ─────────────────────────────────────────────────────────────────────────────────")
    print("    [1] Download a specific package")
    print("    [2] Get update info of package")
    print("    [3] Search for a plugin")
    print("    [4] Download latest version of package")
    print("    [5] Check update for installed plugins")
    print()