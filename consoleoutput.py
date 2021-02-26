# Handles the console output
from os import system
from os import name

def consoleTitle():
    system("title " + "🧱 pluGET by Neocky")


def clearConsole():
    system('cls' if name=='nt' else 'clear')


def printLogo():
    print()
    print(r"          ___           ___       ___           ___           ___           ___     ")
    print(r"         /\  \         /\__\     /\__\         /\  \         /\  \         /\  "'\\    ')
    print(r"        /::\  \       /:/  /    /:/  /        /::\  \       /::\  \        \:\  "'\\   ')
    print(r"       /:/\:\  \     /:/  /    /:/  /        /:/\:\  \     /:/\:\  \        \:\  "'\\  ')
    print(r"      /::\~\:\  \   /:/  /    /:/  /  ___   /:/  \:\  \   /::\~\:\  \       /::\  "'\\')
    print(r"     /:/\:\ \:\__\ /:/__/    /:/__/  /\__\ /:/__/_\:\__\ /:/\:\ \:\__\     /:/\:\__\ ")
    print(r"     \/__\:\/:/  / \:\  \    \:\  \ /:/  / \:\  /\ \/__/ \:\~\:\ \/__/    /:/  \/__/")
    print(r"          \::/  /   \:\  \    \:\  /:/  /   \:\ \:\__\    \:\ \:\__\     /:/  /     ")
    print(r"           \/__/     \:\  \    \:\/:/  /     \:\/:/  /     \:\ \/__/     \/__/      ")
    print(r"                      \:\__\    \::/  /       \::/  /       \:\__\                  ")
    print(r"                       \/__/     \/__/         \/__/         \/__/                  ")
    print()
    print()
    print("                                       by Neocky                                     ")
    print()

def printMainMenu():
    printLogo()
    print("    ─────────────────────────────────────────────────────────────────────────────────")
    print("    [1] Download a specific package")
    print("    [2] Get update info of package")
    print()