""""
	Handles the input through the pluGET command line
"""

from src.utils.utilities import rich_print_error


# check
# update
# get
# get-paper
# get-purpur
# get-airplane
# exit
# remove
# search ???


def handle_input() -> None:
	"""
		Manages the correct function calling from the given input
	"""
	while True:
		try:
			input_command, input_selected_object, input_parameter = get_input()
		except TypeError:
			# KeyboardInterrupt was triggered and None was returned so exit
			return

		match input_command:
			case "get":
				match input_selected_object.isdigit():
					case True:
						print("get specific package")
						#getSpecificPackage(inputSelectedObject, pluginPath,  inputParams)
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
			case _:
				rich_print_error("Error: Command not found. Please try again. :(")
				rich_print_error("Use: 'help command' to get all available commands")


def get_input() -> None:
	"""
		Gets command line input and calls the handle input function
	"""
	input_command = None
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
