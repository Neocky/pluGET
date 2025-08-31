"""
Handles Modrinth plugin checking, downloading and updating
"""

import re
from pathlib import Path

from src.utils.utilities import api_do_request, create_temp_plugin_folder, remove_temp_plugin_folder
from src.utils.console_output import rich_print_error
from src.plugin.plugin_downloader import get_download_path
from src.handlers.handle_config import config_value


def get_modrinth_project_info(project_id: str) -> dict:
    """
    Gets project information from Modrinth API
    
    :param project_id: Modrinth project ID or slug
    :returns: Project information dict or None if failed
    """
    url = f"https://api.modrinth.com/v2/project/{project_id}"
    project_data = api_do_request(url)
    
    if project_data is None:
        return None
    
    if "error" in project_data:
        rich_print_error(f"Error: Modrinth project '{project_id}' not found!")
        return None
        
    return project_data


def get_modrinth_versions(project_id: str, featured_only: bool = False, version_type: str = None) -> list:
    """
    Gets available versions for a Modrinth project
    
    :param project_id: Modrinth project ID or slug
    :param featured_only: Only return featured versions
    :param version_type: Filter by version type (release, beta, alpha)
    :returns: List of versions or None if failed
    """
    url = f"https://api.modrinth.com/v2/project/{project_id}/version"
    
    # Add query parameters like PluginUpdater does
    params = []
    params.append("loaders=[%22bukkit%22,%22spigot%22,%22paper%22,%22purpur%22,%22folia%22]")
    
    if featured_only:
        params.append("featured=true")
    
    if version_type:
        params.append(f"version_type={version_type}")
    
    if params:
        url += "?" + "&".join(params)
    
    versions_data = api_do_request(url)
    
    if versions_data is None:
        return None
    
    if isinstance(versions_data, dict) and "error" in versions_data:
        rich_print_error(f"Error getting versions for Modrinth project '{project_id}': {versions_data['error']}")
        return None
        
    return versions_data


def get_modrinth_plugin_version(project_id: str, featured_only: bool = False, version_type: str = None) -> str:
    """
    Gets the latest plugin version from Modrinth
    
    :param project_id: Modrinth project ID or slug
    :param featured_only: Only consider featured versions
    :param version_type: Filter by version type (release, beta, alpha)
    :returns: Latest version string or None if failed
    """
    versions = get_modrinth_versions(project_id, featured_only, version_type)
    if not versions:
        return None
    
    # Versions are returned sorted by date, newest first
    latest_version = versions[0]
    return latest_version.get("version_number", "")


def get_modrinth_download_url(project_id: str, featured_only: bool = False, version_type: str = None) -> tuple:
    """
    Gets the download URL for the latest Modrinth version
    
    :param project_id: Modrinth project ID or slug  
    :param featured_only: Only consider featured versions
    :param version_type: Filter by version type (release, beta, alpha)
    :returns: Tuple of (download_url, filename) or (None, None) if failed
    """
    versions = get_modrinth_versions(project_id, featured_only, version_type)
    if not versions:
        return None, None
    
    latest_version = versions[0]
    files = latest_version.get("files", [])
    
    if not files:
        rich_print_error(f"Error: No files found in latest version for '{project_id}'!")
        return None, None
    
    # Look for primary file first, then any .jar file
    for file_info in files:
        if file_info.get("primary", False):
            return file_info["url"], file_info["filename"]
    
    for file_info in files:
        if file_info["filename"].endswith(".jar"):
            return file_info["url"], file_info["filename"]
    
    # If no .jar found, return first file
    return files[0]["url"], files[0]["filename"]


def download_modrinth_plugin(project_id: str, featured_only: bool = False, version_type: str = None) -> None:
    """
    Downloads the latest plugin version from Modrinth
    
    :param project_id: Modrinth project ID or slug
    :param featured_only: Only consider featured versions  
    :param version_type: Filter by version type (release, beta, alpha)
    :returns: None
    """
    config_values = config_value()
    download_url, filename = get_modrinth_download_url(project_id, featured_only, version_type)
    
    if download_url is None:
        return None
    
    # Get project info for proper naming
    project_info = get_modrinth_project_info(project_id)
    if project_info is None:
        plugin_name = project_id  # Fallback to project_id
    else:
        plugin_name = project_info.get("title", project_id)
    
    version = get_modrinth_plugin_version(project_id, featured_only, version_type)
    if version is None:
        version = "latest"

    # Create download path with proper SFTP/FTP handling
    if config_values.connection != "local":
        download_path = create_temp_plugin_folder()
    else:
        download_path = get_download_path(config_values)
    # Use original filename if available, otherwise construct one
    if filename:
        plugin_download_name = filename
    else:
        plugin_download_name = f"{plugin_name}-{version}.jar"
    
    download_plugin_path = Path(f"{download_path}/{plugin_download_name}")
    
    # Use existing download infrastructure but with Modrinth URL
    _download_modrinth_file(download_url, download_plugin_path)
    
    return None


def _download_modrinth_file(url: str, download_path: Path) -> None:
    """
    Downloads a file from Modrinth - similar to GitHub download function
    
    :param url: Modrinth file download URL
    :param download_path: Path where to save the file
    :returns: None
    """
    import os
    import requests
    from zipfile import ZipFile
    from rich.console import Console
    from rich.progress import Progress
    from src.utils.utilities import convert_file_size_down, remove_temp_plugin_folder
    from src.handlers.handle_sftp import sftp_create_connection, sftp_upload_file
    from src.handlers.handle_ftp import ftp_create_connection, ftp_upload_file
    
    config_values = config_value()
    
    # Use rich Progress() to create progress bar (same as existing implementations)
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

    # use rich console for nice colors (consistent with existing style)
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

    # Handle SFTP/FTP upload same as existing implementations
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


def search_modrinth_plugin(search_term: str) -> None:
    """
    Search for plugins on Modrinth
    
    :param search_term: Search query
    :returns: None
    """
    from rich.table import Table
    from rich.console import Console
    
    # Modrinth search API with filters for plugins
    url = f"https://api.modrinth.com/v2/search?query={search_term}&facets=[[%22categories:bukkit%22],[%22categories:spigot%22],[%22categories:paper%22]]&sort=downloads"
    search_results = api_do_request(url)
    
    if search_results is None:
        rich_print_error("Error: Modrinth search request failed!")
        return None
    
    hits = search_results.get("hits", [])
    if not hits:
        rich_print_error(f"No plugins found for '{search_term}' on Modrinth")
        return None
    
    # Limit to top 10 results
    hits = hits[:10]
    
    print(f"Searching Modrinth for '{search_term}'...")
    print(f"Found plugins:")
    
    # Create table with rich (same style as existing search functions)
    rich_table = Table(box=None)
    rich_table.add_column("No.", justify="right", style="cyan", no_wrap=True)
    rich_table.add_column("Name", style="bright_magenta")
    rich_table.add_column("Downloads", justify="right", style="bright_green")
    rich_table.add_column("Description", justify="left", style="white")
    
    # Start counting at 1 for consistency with existing code
    i = 1
    for plugin in hits:
        plugin_name = plugin["title"]
        downloads = plugin.get("downloads", 0)
        description = plugin.get("description", "No description") or "No description"
        # Truncate long descriptions
        if len(description) > 50:
            description = description[:47] + "..."
        rich_table.add_row(str(i), plugin_name, str(downloads), description)
        i += 1

    # Print table from rich
    rich_console = Console()
    rich_console.print(rich_table)

    try:
        plugin_selected = input("Select your wanted plugin (No.)(0 to exit): ")
    except KeyboardInterrupt:
        return None
    if plugin_selected == "0":
        return None
    try:
        plugin_selected = int(plugin_selected) - 1
        selected_plugin = hits[plugin_selected]
    except ValueError:
        rich_print_error("Error: Input wasn't a number! Please try again!")
        return None
    except IndexError:
        rich_print_error("Error: Number was out of range! Please try again!")
        return None
        
    selected_plugin_name = selected_plugin["title"]
    selected_project_id = selected_plugin["project_id"]
    rich_console.print(f"\n [not bold][bright_white]● [bright_magenta]{selected_plugin_name} [bright_green]latest")
    download_modrinth_plugin(selected_project_id)

    return None


def get_modrinth_project_from_plugin_hash(plugin_file_path: str) -> str:
    """
    Try to identify a Modrinth project from a plugin file hash
    This mimics the PluginUpdater approach of using file hashes
    
    :param plugin_file_path: Path to the plugin .jar file
    :returns: Project ID if found, None otherwise
    """
    import hashlib
    
    try:
        with open(plugin_file_path, 'rb') as f:
            file_data = f.read()
            file_hash = hashlib.sha512(file_data).hexdigest()
    except (FileNotFoundError, OSError):
        return None
    
    # Use Modrinth's version_files endpoint to lookup by hash
    url = "https://api.modrinth.com/v2/version_files"
    payload = {
        "algorithm": "sha512",
        "hashes": [file_hash]
    }
    
    # Need to make a POST request for hash lookup
    import requests
    import json
    
    try:
        response = requests.post(url, 
                               json=payload,
                               headers={'user-agent': 'pluGET/1.0', 'Content-Type': 'application/json'})
        if response.status_code == 200:
            result = response.json()
            if file_hash in result:
                version_info = result[file_hash]
                return version_info.get("project_id")
    except (requests.RequestException, json.JSONDecodeError):
        pass
    
    return None
