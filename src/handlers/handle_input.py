""""
Handles the input through the pluGET command line
"""

from src.utils.console_output import rich_print_error
from src.plugin.plugin_downloader import get_specific_plugin, search_specific_plugin
from src.plugin.plugin_updatechecker import check_installed_plugins, update_installed_plugins


# check
# update
# get
# get-paper
# get-purpur ???
# get-airplane ???
# exit
# remove
# search


def handle_input(
    input_command : str=None,
    input_selected_object : str=None,
    input_parameter : str=None,
    no_confirmation : bool=False,
    arguments_from_console : bool=False
    ) -> None:
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
                        search_specific_plugin(input_selected_object)

            case "update":
                match input_selected_object:
                    case "serverjar":
                        print("update serverjar")
                        #updateServerjar(inputParams)
                    case _:
                        update_installed_plugins(input_selected_object, no_confirmation)

            case "check":
                match input_selected_object:
                    case "serverjar":
                        print("check serverjar")
                        #checkInstalledServerjar()
                    case _:
                        check_installed_plugins(input_selected_object, input_parameter)

            case "search":
                search_specific_plugin(input_selected_object)
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
    print("\n'STRG + C' to exit")
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
