"""
	Handles the console on first startup of pluGET and prints logo and sets title
"""

import os
from rich.console import Console


def rename_console_title() -> None:
	"""
		Renames the console title on first startup
	"""
	os.system("title " + "pluGET │ By Neocky")


def clear_console() -> None:
	"""
		Clears the console on first startup
	"""
	os.system('cls' if os.name=='nt' else 'clear')

def print_logo() -> None:
	console = Console()
	# line 1
	console.print()
	# line 2
	console.print("    ██████",style="bright_magenta", end='')
	console.print("╗ ", style="bright_yellow", end='')
	console.print("██", style="bright_magenta", end='')
	console.print("╗     ", style="bright_yellow", end='')
	console.print("██", style="bright_magenta", end='')
	console.print("╗   ", style="bright_yellow", end='')
	console.print("██", style="bright_magenta", end='')
	console.print("╗ ", style="bright_yellow", end='')
	console.print("██████", style="bright_magenta", end='')
	console.print("╗ ", style="bright_yellow", end='')
	console.print("███████", style="bright_magenta", end='')
	console.print("╗", style="bright_yellow", end='')
	console.print("████████", style="bright_magenta", end='')
	console.print("╗", style="bright_yellow")
	# line 3
	console.print("    ██", style="bright_magenta", end='')
	console.print("╔══", style="bright_yellow", end='')
	console.print("██", style="bright_magenta", end='')
	console.print("╗",	style="bright_yellow", end='')
	console.print("██", style="bright_magenta", end='')
	console.print("║     ", style="bright_yellow", end='')
	console.print("██", style="bright_magenta", end='')
	console.print("║   ", style="bright_yellow", end='')
	console.print("██", style="bright_magenta", end='')
	console.print("║", style="bright_yellow", end='')
	console.print("██", style="bright_magenta", end='')
	console.print("╔════╝ ", style="bright_yellow", end='')
	console.print("██", style="bright_magenta", end='')
	console.print("╔════╝╚══", style="bright_yellow", end='')
	console.print("██", style="bright_magenta", end='')
	console.print("╔══╝", style="bright_yellow")
	# line 4
	console.print("    ██████╔╝██║     ██║   ██║██║  ███╗█████╗     ██║   ")
	# line 5
	console.print("    ██╔═══╝ ██║     ██║   ██║██║   ██║██╔══╝     ██║   ")
	# line 6
	console.print("    ██║     ███████╗╚██████╔╝╚██████╔╝███████╗   ██║   ")
	# line 7
	console.print("    ╚═╝     ╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   ", style="bright_yellow")


	console.print("                        ┌────────────────────────────────────┐", style="bright_black")
    #print("                        │             [" + oColors.brightMagenta + "By Neocky" +oColors.brightBlack +
    # "]            │                                   " + oColors.standardWhite)
    #print(oColors.brightBlack + "                        │  " + oColors.brightMagenta + "https://github.com/Neocky/pluGET" + oColors.brightBlack +
    # "  │                                                  " + oColors.standardWhite)
    #print(oColors.brightBlack + "                        └────────────────────────────────────┘" + oColors.standardWhite)
