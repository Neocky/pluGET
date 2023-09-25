""""
Handles the input through the pluGET command line
"""

from src.utils.console_output import rich_print_error
from src.utils.utilities import get_command_help
from src.plugin.plugin_remover import delete_plugin
from src.plugin.plugin_downloader import get_specific_plugin_spiget, search_specific_plugin_spiget
from src.plugin.plugin_updatechecker import check_installed_plugins, update_installed_plugins
from src.serverjar.serverjar_updatechecker import \
   check_update_available_installed_server_jar, update_installed_server_jar
from src.serverjar.serverjar_paper_velocity_waterfall import serverjar_papermc_update
from src.serverjar.serverjar_purpur import serverjar_purpur_update
from src.handlers.handle_server import server_list
from src.handlers import handle_server


# server
# check
# update
# get
# get-paper
# get-waterfall
# get-velocity
# get-purpur
# exit
# remove
# search
# help


def handle_input(
    input_command : str=None,
    input_selected_object : str=None,
    input_parameter : str=None,
    no_confirmation : bool=False,
    arguments_from_console : bool=False
    ) -> None:
    """
    Manages the correct function calling from the given input

    :param input_command: Command of main function
    :param input_selected_object: Name of plugin/serverjar
    :param: input_parameter: Optional parameters
    :param no_confirmation: If plugins should be updated without no confirmation message
    :param arguments_from_console: If arguments were given on script call

    :returns None:
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
            case "server":
                match input_selected_object:
                    case "is":
                        print(handle_server.active_server.name)
                    case _:
                        try:
                            handle_server.active_server = server_list[input_selected_object]
                            print("Set to "+handle_server.active_server.name)
                        except KeyError:
                            print("Invalid server name")
                
            case "get":
                match input_selected_object.isdigit():
                    case True:
                        get_specific_plugin_spiget(input_selected_object, input_parameter)
                    case _:
                        search_specific_plugin_spiget(input_selected_object)

            case "get-paper":
                serverjar_papermc_update(input_selected_object, input_parameter, None, "paper")
            case "get-velocity":
                serverjar_papermc_update(input_selected_object, input_parameter, None, "velocity")
            case "get-waterfall":
                serverjar_papermc_update(input_selected_object, input_parameter, None, "waterfall")
            case "get-purpur":
                serverjar_purpur_update(input_selected_object, input_parameter, None)

            case "update":
                match input_selected_object:
                    case "serverjar":
                        update_installed_server_jar(input_parameter)
                    case _:
                        update_installed_plugins(input_selected_object, no_confirmation)

            case "check":
                match input_selected_object:
                    case "serverjar":
                        check_update_available_installed_server_jar()
                    case _:
                        check_installed_plugins(input_selected_object, input_parameter)

            case "search":
                search_specific_plugin_spiget(input_selected_object)
            case "remove":
                delete_plugin(input_selected_object)
            case "help":
                get_command_help(input_selected_object)
            case "exit":
                return
            case _:
                rich_print_error("Error: Command not found. Please try again. :(")
                rich_print_error("Use [bright_blue]'help all' [bright_red]to get a list of all available commands.")

        # return to break out of while loop if pluGET was started with arguments from console
        if arguments_from_console:
            return None


def get_input() -> str:
    """
    Gets command line input and calls the handle input function

    :returns: Main command to execute
    :returns: Selected Object to work with
    :returns: Optional parameter
    """
    input_command = None
    # print("\n'STRG + C' to exit")
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
                rich_print_error("Use: [bright_blue]'help all' [bright_red]to get a list of all available commands.")
        except KeyboardInterrupt:
            return
    input_parameter = input_parameter[0] if input_parameter else None
    return input_command, input_selected_object, input_parameter
