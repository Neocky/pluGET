# Main function for pluGET
import argparse

from src.handlers.handle_config import check_config, config_value


if __name__ == "__main__":
	check_config()
    #check_requirements()
	parser = argparse.ArgumentParser(description="Just an example",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	#parser.add_argument("-a", "--archive", action="store_true", help="archive mode")
	#parser.add_argument("--exclude", help="files to exclude")
	parser.add_argument("mode", help="Mode (install/update)", nargs='?', default=None)
	parser.add_argument("plugin", help="Plugin Name", nargs='?', default=None)
	args = vars(parser.parse_args())
	if args["mode"] is not None and args["plugin"] is not None:
		#argument_code(args["mode"], args["plugin"])
		print("arguments")
	
	else:
		print("no arguments")
		#consoleTitle()
		#clearConsole()
		#createInputLists()
		#printMainMenu()
		#getInput()
	config = config_value()
	print(config.connection)
	print(config.path_to_plugin_folder)
	print(config.sftp_port)
	print(config.local_seperate_download_path)

