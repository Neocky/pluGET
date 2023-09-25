"""
Handles the update checking and downloading of these serverjars:
Purpur
"""

import re
import requests
from pathlib import Path
from rich.table import Table
from rich.console import Console
from rich.progress import Progress

from src.utils.console_output import rich_print_error
from src.handlers import handle_server
from src.utils.utilities import \
    api_do_request, create_temp_plugin_folder, remove_temp_plugin_folder, convert_file_size_down
from src.serverjar.serverjar_paper_velocity_waterfall import \
     get_installed_serverjar_version, get_version_group, get_versions_behind


def find_latest_available_version(version_group) -> int:
    """
    Gets the latest available version of the installed serverjar version

    :param version_group: Minecraft version group of the serverjar

    :returns: Latest available version as int
    """
    url = f"https://api.purpurmc.org/v2/purpur/{version_group}/"
    versions = api_do_request(url)
    if "status" in versions: # Checks if the API returns a status. This means that there was an error.
        return None
    latest_version = versions["builds"]["all"][-1]
    return latest_version


def get_purpur_download_file_name(mc_version, serverjar_version) -> str:
    """
    Gets the download name from the purpur api and merge it together in the right format

    :param mc_version: Minecraft version
    :param serverjar_version: Version of the serverjar
    :param file_server_jar_full_name: Serverjar name

    :returns: Download name of the file
    """
    url = f"https://api.purpurmc.org/v2/purpur/{mc_version}/{serverjar_version}/"
    build_details = api_do_request(url)
    purpur_build_version = build_details["build"]
    purpur_project_name = build_details["project"]
    purpur_mc_version = build_details["version"]
    download_name = f"{purpur_project_name}-{purpur_mc_version}-{purpur_build_version}.jar"
    return download_name


def serverjar_purpur_check_update(file_server_jar_full_name) -> None:
    """
    Checks the installed purpur serverjar if an update is available
    
    :param file_server_jar_full_name: Full name of the purpu server jar file name

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

    latest_version = find_latest_available_version(version_group)
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


def serverjar_purpur_update(
    server_jar_version: str="latest",
    mc_version: str=None,
    file_server_jar_full_name: str=None
    ) -> bool:
    """
    Handles the downloading of the papermc serverjar

    :param server_jar_version: Version of the serverjar which should get downloaded
    :param mc_version: Minecraft version
    :param no_confirmation: If no confirmation message should pop up
    :param file_server_jar_full_name: The old serverjar file

    :returns: True/False if the serverjar was downloaded successfully
    """

    path_server_root = create_temp_plugin_folder()

    # exit if the mc version can't be found
    if file_server_jar_full_name == None and mc_version == None:
        rich_print_error("Error: Please specifiy the minecraft version as third argument!")
        return False

    if mc_version == None:
        mc_version = get_version_group(file_server_jar_full_name)

    if server_jar_version == "latest" or server_jar_version == None:
        server_jar_version = find_latest_available_version(mc_version)

    if file_server_jar_full_name == None:
        serverjar_name = "purpur"
    else:
        serverjar_name = file_server_jar_full_name

    # use rich console for nice colors
    rich_console = Console()
    rich_console.print(
        f"\n [not bold][bright_white]● [bright_magenta]{serverjar_name.capitalize()}" + \
        f" [cyan]→ [bright_green]{server_jar_version}"
    )

    if file_server_jar_full_name != None:
        serverjar_version = get_installed_serverjar_version(file_server_jar_full_name)
        if get_versions_behind(serverjar_version, server_jar_version) == 0:
            rich_console.print("    [not bold][bright_green]No updates currently available!")
            return False

    try:
        download_file_name = get_purpur_download_file_name(mc_version, server_jar_version)
    except KeyError:
        rich_print_error(f"    Error: This version wasn't found for {mc_version}")
        rich_print_error(f"    Reverting to latest version for {mc_version}")
        try:
            server_jar_version = find_latest_available_version(mc_version)
            download_file_name = get_purpur_download_file_name(mc_version, server_jar_version)
        except KeyError:
            rich_print_error(
                f"    Error: Version {mc_version} wasn't found for {serverjar_name.capitalize()} in the purpur api"
            )
            return False

    url = f"https://api.purpurmc.org/v2/purpur/{mc_version}/{server_jar_version}/download/"
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
