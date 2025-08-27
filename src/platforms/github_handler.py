"""
Handles GitHub plugin checking, downloading and updating
"""

import re
from pathlib import Path

from src.utils.utilities import api_do_request, create_temp_plugin_folder, remove_temp_plugin_folder
from src.utils.console_output import rich_print_error
from src.plugin.plugin_downloader import get_download_path, download_specific_plugin_version_spiget
from src.handlers.handle_config import config_value


def get_github_repo_from_plugin_name(plugin_name: str) -> str:
    """
    Tries to guess GitHub repository from plugin name
    This is a fallback function - ideally users should provide the full repo path
    
    :param plugin_name: Name of the plugin
    :returns: Guessed repository path or None if not found
    """
    # This is a basic implementation - could be enhanced with a mapping file
    # For now, return None to encourage explicit repo specification
    return None


def get_latest_github_release(github_repo: str) -> dict:
    """
    Gets the latest GitHub release information
    
    :param github_repo: Repository path in format 'owner/repo'
    :returns: Release information dict or None if failed
    """
    url = f"https://api.github.com/repos/{github_repo}/releases/latest"
    release_data = api_do_request(url)
    
    if release_data is None:
        return None
    
    if "message" in release_data and release_data["message"] == "Not Found":
        rich_print_error(f"Error: GitHub repository '{github_repo}' not found!")
        return None
        
    return release_data


def get_github_plugin_version(github_repo: str) -> str:
    """
    Gets the latest plugin version from GitHub releases
    
    :param github_repo: Repository path in format 'owner/repo'
    :returns: Latest version string or None if failed
    """
    release_data = get_latest_github_release(github_repo)
    if release_data is None:
        return None
        
    version = release_data.get("tag_name", "")
    # Remove 'v' prefix if present (e.g., 'v1.0.0' -> '1.0.0')
    version = re.sub(r'^v', '', version)
    return version


def get_github_download_url(github_repo: str) -> str:
    """
    Gets the download URL for the latest GitHub release
    
    :param github_repo: Repository path in format 'owner/repo'
    :returns: Download URL or None if failed
    """
    release_data = get_latest_github_release(github_repo)
    if release_data is None:
        return None
        
    assets = release_data.get("assets", [])
    if not assets:
        rich_print_error(f"Error: No assets found in latest release for '{github_repo}'!")
        return None
    
    # Look for .jar file first
    for asset in assets:
        if asset["name"].endswith(".jar"):
            return asset["browser_download_url"]
    
    # If no .jar found, return first asset
    return assets[0]["browser_download_url"]


def download_github_plugin(github_repo: str, plugin_name: str = None) -> None:
    """
    Downloads the latest plugin version from GitHub releases
    
    :param github_repo: Repository path in format 'owner/repo'
    :param plugin_name: Optional plugin name override
    :returns: None
    """
    config_values = config_value()
    download_url = get_github_download_url(github_repo)
    
    if download_url is None:
        return None
    
    # Extract plugin name from repo if not provided
    if plugin_name is None:
        plugin_name = github_repo.split('/')[-1]
    
    version = get_github_plugin_version(github_repo)
    if version is None:
        version = "latest"

    # Create download path with proper SFTP/FTP handling
    if config_values.connection != "local":
        download_path = create_temp_plugin_folder()
    else:
        download_path = get_download_path(config_values)
    plugin_download_name = f"{plugin_name}-{version}.jar"
    download_plugin_path = Path(f"{download_path}/{plugin_download_name}")
    
    # Use existing download infrastructure but with GitHub URL
    _download_github_file(download_url, download_plugin_path)
    
    return None


def _download_github_file(url: str, download_path: Path) -> None:
    """
    Downloads a file from GitHub releases - similar to download_specific_plugin_version_spiget
    
    :param url: GitHub asset download URL  
    :param download_path: Path where to save the file
    :returns: None
    """
    import os
    import requests
    from zipfile import ZipFile
    from rich.console import Console
    from rich.progress import Progress
    from src.utils.utilities import convert_file_size_down
    from src.handlers.handle_sftp import sftp_create_connection, sftp_upload_file
    from src.handlers.handle_ftp import ftp_create_connection, ftp_upload_file
    
    config_values = config_value()
    
    # Use rich Progress() to create progress bar (same as spiget implementation)
    with Progress(transient=True) as progress:
        header = {'user-agent': 'pluGET/1.0'}
        r = requests.get(url, headers=header, stream=True)
        try:
            file_size = int(r.headers.get('content-length'))
            # create progress bar
            download_task = progress.add_task("    [cyan]Downloading...", total=file_size)
        except TypeError:
            # Content-length returned nothing
            file_size = 0
        with open(download_path, 'wb') as f:
            # split downloaded data in chunks of 32768
            for data in r.iter_content(chunk_size=32768):
                f.write(data)
                # don't show progress bar if no content-length was returned
                if file_size == 0:
                    continue
                progress.update(download_task, advance=len(data))

    # use rich console for nice colors (same style as existing code)
    console = Console()
    if file_size == 0:
        console.print(
            f"    [not bold][bright_green]Downloaded[bright_magenta]         file [cyan]→ [white]{download_path}"
        )
    elif file_size >= 1000000:
        file_size_data = convert_file_size_down(convert_file_size_down(file_size))
        console.print("    [not bold][bright_green]Downloaded[bright_magenta] " + (str(file_size_data)).rjust(9) + \
             f" MB [cyan]→ [white]{download_path}")
    else:
        file_size_data = convert_file_size_down(file_size)
        console.print("    [not bold][bright_green]Downloaded[bright_magenta] " + (str(file_size_data)).rjust(9) + \
             f" KB [cyan]→ [white]{download_path}")

    # check if plugin file is a proper .jar-file (try to open plugin.yml or paper-plugin.yml file)
    # updated validation to support both plugin.yml and paper-plugin.yml
    plugin_valid = False
    try:
        with ZipFile(download_path, "r") as plugin_jar:
            try:
                plugin_jar.open("plugin.yml", "r")
                plugin_valid = True
            except KeyError:
                try:
                    plugin_jar.open("paper-plugin.yml", "r")
                    plugin_valid = True
                except KeyError:
                    pass
    except:
        pass
    
    if not plugin_valid:
        rich_print_error("Error: Downloaded plugin file was not a proper jar-file!")
        rich_print_error("Removing file...")
        os.remove(download_path)
        return None

    # Handle SFTP/FTP upload same as existing implementation
    if config_values.connection == "sftp":
        sftp_session = sftp_create_connection()
        sftp_upload_file(sftp_session, download_path)
    elif config_values.connection == "ftp":
        ftp_session = ftp_create_connection()
        ftp_upload_file(ftp_session, download_path)

    # remove temp plugin folder if plugin was downloaded from sftp/ftp server
    if config_values.connection != "local":
        remove_temp_plugin_folder()

    return None


def search_github_plugin(search_term: str) -> None:
    """
    Search for plugins on GitHub (basic implementation)
    GitHub doesn't have a plugin-specific search, so this searches for Java repositories
    
    :param search_term: Search query
    :returns: None
    """
    from rich.table import Table
    from rich.console import Console
    
    url = f"https://api.github.com/search/repositories?q={search_term}+language:java+spigot&sort=stars&order=desc"
    search_results = api_do_request(url)
    
    if search_results is None:
        rich_print_error("Error: GitHub search request failed!")
        return None
    
    if search_results.get("total_count", 0) == 0:
        rich_print_error(f"No repositories found for '{search_term}'")
        return None
    
    repositories = search_results.get("items", [])[:10]  # Limit to top 10
    
    print(f"Searching GitHub for '{search_term}'...")
    print(f"Found repositories:")
    
    # Create table with rich (same style as existing search)
    rich_table = Table(box=None)
    rich_table.add_column("No.", justify="right", style="cyan", no_wrap=True)
    rich_table.add_column("Repository", style="bright_magenta")
    rich_table.add_column("Stars", justify="right", style="bright_green") 
    rich_table.add_column("Description", justify="left", style="white")
    
    # Start counting at 1 for consistency with existing code
    i = 1
    for repo in repositories:
        repo_name = repo["full_name"]
        stars = repo["stargazers_count"]
        description = repo.get("description", "No description") or "No description"
        # Truncate long descriptions
        if len(description) > 50:
            description = description[:47] + "..."
        rich_table.add_row(str(i), repo_name, str(stars), description)
        i += 1

    # Print table from rich
    rich_console = Console()
    rich_console.print(rich_table)

    try:
        plugin_selected = input("Select your wanted repository (No.)(0 to exit): ")
    except KeyboardInterrupt:
        return None
    if plugin_selected == "0":
        return None
    try:
        plugin_selected = int(plugin_selected) - 1
        selected_repo = repositories[plugin_selected]["full_name"]
    except ValueError:
        rich_print_error("Error: Input wasn't a number! Please try again!")
        return None
    except IndexError:
        rich_print_error("Error: Number was out of range! Please try again!")
        return None
        
    selected_repo_name = selected_repo.split('/')[-1]
    rich_console.print(f"\n [not bold][bright_white]● [bright_magenta]{selected_repo_name} [bright_green]latest")
    download_github_plugin(selected_repo, selected_repo_name)

    return None
