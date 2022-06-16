""""
Handles the input through the pluGET command line
"""

from src.utils.console_output import rich_print_error
from src.plugin.plugin_downloader import get_specific_plugin


# check
# update
# get
# get-paper
# get-purpur
# get-airplane
# exit
# remove
# search ???


def handle_input(input_command=None, input_selected_object=None, input_parameter=None, arguments_from_console=False) -> None:
	"""
	Manages the correct function calling from the given input
	"""
	while True:
		# when arguemnts were not passed from console ask for input
		if arguments_from_console is False:
			try:
				input_command, input_selected_object, input_parameter = get_input()
			except TypeError:
				# KeyboardInterrupt was triggered and None was returned so exit
				return

		match input_command:
			case "get":
				match input_selected_object.isdigit():
					case True:
						get_specific_plugin(input_selected_object, input_parameter)
					case _:
						print("get search specific package")
						#searchPackage(inputSelectedObject)

			case "update":
				print("update package")
				match input_selected_object:
					case "serverjar":
						print("update serverjar")
						#updateServerjar(inputParams)
					case _:
						print("update package")
						#updateInstalledPackage(inputSelectedObject)

			case "check":
				print("check package")
				match input_selected_object:
					case "serverjar":
						print("check serverjar")
						#checkInstalledServerjar()
					case _:
						print("check plugins")
						#checkInstalledPackage(inputSelectedObject, inputParams)

			case "search":
				print("search package")
				#searchPackage(inputSelectedObject)
			case "remove":
				print("remove package")
				#removePlugin(inputSelectedObject)
			case "get-paper":
				# download papermc
				print("download papermc")
				#papermc_downloader(inputSelectedObject, inputParams)
			case "exit":
				return
			case _:
				rich_print_error("Error: Command not found. Please try again. :(")
				rich_print_error("Use: 'help command' to get all available commands")

		# return to break out of while loop if pluGET was started with arguments from console
		if arguments_from_console:
			return None


def get_input() -> None:
	"""
		Gets command line input and calls the handle input function
	"""
	input_command = None
	print("'STRG + C' to exit")
	while True:
		try:
			input_command, input_selected_object, *input_parameter = input("pluGET >> ").split()
			break
		except ValueError:
			if input_command == None:
				# request input again if no input was given or not enough
				continue
			else:
				rich_print_error("Wrong input! Use: > 'command' 'selectedObject' [optionalParams]")
				rich_print_error("Use: 'help command' to get all available commands")
		except KeyboardInterrupt:
			return
	input_parameter = input_parameter[0] if input_parameter else None
	return input_command, input_selected_object, input_parameter
