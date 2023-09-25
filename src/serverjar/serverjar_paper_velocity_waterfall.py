"""
Handles the update checking and downloading of these serverjars:
Paper, Velocity, Waterfall

All are from the PaperMC Team and use the same api structure which is the reason these are together
"""

import re
import requests
from pathlib import Path
from rich.table import Table
from rich.console import Console
from rich.progress import Progress
from src.handlers import handle_server

# from src.handlers.handle_config import config_value
from src.utils.console_output import rich_print_error
# from src.handlers.handle_sftp import sftp_create_connection, sftp_upload_server_jar
# from src.handlers.handle_ftp import ftp_create_connection, ftp_upload_server_jar
from src.utils.utilities import \
    api_do_request, create_temp_plugin_folder, remove_temp_plugin_folder, convert_file_size_down


def get_installed_serverjar_version(file_server_jar_full_name) -> str:
    """
    Gets the installed version of the installed serverjar

    :param file_server_jar_full_name: Full file name fo the installed serverjar

    :returns: Used serverjar version
    """
    serverjar_version_full = re.search(r"([\d]*.jar)", file_server_jar_full_name)
    try:
        serverjar_version = serverjar_version_full.group()
    except AttributeError:
        serverjar_version = serverjar_version_full
    serverjar_version = serverjar_version.replace('.jar', '')

    return serverjar_version


def get_version_group(file_server_jar_full_name) -> str:
    """
    Gets the version group which is used for the papermc api

    :param mc_version: Version of Minecraft in use

    :returns: Version group of api
    """
    version_group = re.sub(r"-\d*.jar$", "", file_server_jar_full_name)
    version_group = re.sub(r"^(\w*\-)", "", version_group)
    return version_group


def find_latest_available_version(file_server_jar_full_name, version_group) -> int:
    """
    Gets the latest available version of the installed serverjar version

    :param version_group: Minecraft version group of the serverjar

    :returns: Latest available version as int
    """
    if "paper" in file_server_jar_full_name:
        url = f"https://papermc.io/api/v2/projects/paper/versions/{version_group}/builds"
    elif "waterfall" in file_server_jar_full_name:
        url = f"https://papermc.io/api/v2/projects/waterfall/versions/{version_group}/builds"
    elif "velocity" in file_server_jar_full_name:
        url = f"https://papermc.io/api/v2/projects/velocity/versions/{version_group}/builds"

    versions = api_do_request(url)
    if "status" in versions: # Checks if the API returns a status. This means that there was an error.
        return None
    latest_version = versions["builds"][-1]["build"]
    return latest_version


def get_versions_behind(serverjar_version, latest_version) -> int:
    """
    Gets the number diffference between the two versions

    :param serverjar_version: Installed serverjar version
    :param latest_version: Latest avaialable serverjar version

    :returns: Number difference between the two versions
    """
    versions_behind = int(latest_version) - int(serverjar_version)
    return versions_behind


def get_papermc_download_file_name(mc_version, serverjar_version, file_server_jar_full_name) -> str:
    """
    Gets the download name from the papermc api

    :param mc_version: Minecraft version
    :param serverjar_version: Version of the serverjar
    :param file_server_jar_full_name: Serverjar name

    :returns: Download name of the file
    """
    if "paper" in file_server_jar_full_name:
        url = f"https://papermc.io/api/v2/projects/paper/versions/{mc_version}/builds/{serverjar_version}"
    elif "waterfall" in file_server_jar_full_name:
        url = f"https://papermc.io/api/v2/projects/waterfall/versions/{mc_version}/builds/{serverjar_version}"
    elif "velocity" in file_server_jar_full_name:
        url = f"https://papermc.io/api/v2/projects/velocity/versions/{mc_version}/builds/{serverjar_version}"
    build_details = api_do_request(url)
    download_name = build_details["downloads"]["application"]["name"]
    return download_name


def serverjar_papermc_check_update(file_server_jar_full_name) -> None:
    """
    Checks the installed paper serverjar if an update is available
    
    :param file_server_jar_full_name: Full name of the paper server jar file name

    :returns: None
    """
    serverjar_version = get_installed_serverjar_version(file_server_jar_full_name)
    if serverjar_version == None:
        rich_print_error("Error: An error occured while checking the installed serverjar version")
        return None
    
    version_group = get_version_group(file_server_jar_full_name)
    if version_group == None:
        rich_print_error(
            "Error: An error occured while checking the installed version group of the installed serverjar"
        )
        return None

    latest_version = find_latest_available_version(file_server_jar_full_name, version_group)
    if latest_version == None:
        rich_print_error("Error: An error occured while checking for the latest available version of the serverjar")
        return None

    versions_behind = get_versions_behind(serverjar_version, latest_version)

    rich_table = Table(box=None)
    rich_table.add_column("Name", style="bright_magenta")
    rich_table.add_column("Installed V.", justify="right", style="green")
    rich_table.add_column("Latest V.", justify="right", style="bright_green")
    rich_table.add_column("Versions behind", justify="right", style="cyan")

    rich_table.add_row(
            file_server_jar_full_name, 
            serverjar_version, 
            str(latest_version), 
            str(versions_behind) 
        )
    rich_console = Console()
    rich_console.print(rich_table)
    return None


def serverjar_papermc_update(
    server_jar_version: str="latest",
    mc_version: str=None,
    file_server_jar_full_name: str=None,
    serverjar_to_download: str=None
    ) -> bool:
    """
    Handles the downloading of the papermc serverjar

    :param server_jar_version: Version of the serverjar which should get downloaded
    :param mc_version: Minecraft version
    :param no_confirmation: If no confirmation message should pop up
    :param file_server_jar_full_name: The old serverjar file
    :param serverjar_to_download: The serverjar to download because it supports: paper, velocity, waterfall
                                This is used in the handle_input function

    :returns: True/False if the serverjar was downloaded successfully
    """

    path_server_root = create_temp_plugin_folder()

    # exit if the mc version can't be found
    if file_server_jar_full_name == None and mc_version == None:
        rich_print_error("Error: Please specifiy the minecraft version as third argument!")
        return False

    # if both the file name and the serverjar_to_download are emtpy then exit
    if file_server_jar_full_name == None and serverjar_to_download == None:
        rich_print_error("Error: Couldn't get serverjar name to download")
        return False

    if mc_version == None:
        mc_version = get_version_group(file_server_jar_full_name)

    if file_server_jar_full_name == None:
        papermc_serverjar = serverjar_to_download
    else:
        papermc_serverjar = file_server_jar_full_name

    if server_jar_version == "latest" or server_jar_version == None:
        server_jar_version = find_latest_available_version(papermc_serverjar, mc_version)

    # use rich console for nice colors
    rich_console = Console()
    rich_console.print(
        f"\n [not bold][bright_white]● [bright_magenta]{papermc_serverjar.capitalize()}" + \
        f" [cyan]→ [bright_green]{server_jar_version}"
    )

    if file_server_jar_full_name != None:
        serverjar_version = get_installed_serverjar_version(file_server_jar_full_name)
        if get_versions_behind(serverjar_version, server_jar_version) == 0:
            rich_console.print("    [not bold][bright_green]No updates currently available!")
            return False

    try:
        download_file_name = get_papermc_download_file_name(mc_version, server_jar_version, papermc_serverjar)
    except KeyError:
        rich_print_error(f"    Error: This version wasn't found for {mc_version}")
        rich_print_error(f"    Reverting to latest version for {mc_version}")
        try:
            server_jar_version = find_latest_available_version(papermc_serverjar, mc_version)
            download_file_name = get_papermc_download_file_name(mc_version, server_jar_version, papermc_serverjar)
        except KeyError:
            rich_print_error(
                f"    Error: Version {mc_version} wasn't found for {papermc_serverjar.capitalize()} in the papermc api"
            )
            return False

    if "paper" in papermc_serverjar:
        url = f"https://papermc.io/api/v2/projects/paper/versions/{mc_version}" + \
            f"/builds/{server_jar_version}/downloads/{download_file_name}"
    elif "waterfall" in papermc_serverjar:
        url = f"https://papermc.io/api/v2/projects/waterfall/versions/{mc_version}" + \
            f"/builds/{server_jar_version}/downloads/{download_file_name}"
    elif "velocity" in papermc_serverjar:
        url = f"https://papermc.io/api/v2/projects/velocity/versions/{mc_version}" + \
            f"/builds/{server_jar_version}/downloads/{download_file_name}"
    
    download_path = Path(f"{path_server_root}/{download_file_name}")

    with Progress(transient=True) as progress:
        header = {'user-agent': 'pluGET/1.0'}
        r = requests.get(url, headers=header, stream=True)
        try:
            file_size = int(r.headers.get('Content-Length'))
            # create progress bar
            download_task = progress.add_task("    [cyan]Downloading...", total=file_size)
        except TypeError:
            # Content-lenght returned nothing
            file_size = 0
        with open(download_path, 'wb') as f:
            # split downloaded data in chunks of 65536
            for data in r.iter_content(chunk_size=65536):
                f.write(data)
                # don't show progress bar if no content-length was returned
                if file_size == 0:
                    continue
                progress.update(download_task, advance=len(data))
                #f.flush()

    
    file_size_data = convert_file_size_down(convert_file_size_down(file_size))
    rich_console.print("    [not bold][bright_green]Downloaded[bright_magenta] " + (str(file_size_data)).rjust(9) + \
        f" MB [cyan]→ [white]{download_path}")
        
    handle_server.active_server.create_connection()
    handle_server.active_server.upload_server_jar(download_path)
    remove_temp_plugin_folder()

    return True
