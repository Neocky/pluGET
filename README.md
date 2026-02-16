
<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/branding/pluget-logo-white.png">
  <source media="(prefers-color-scheme: light)" srcset="./assets/branding/pluget-logo-black.png">
  <img src="./assets/branding/pluget-logo-black.png" alt="pluGET" border="0">
</picture>
</p>

<p align="center">  
<a href="https://github.com/Neocky/pluGET/releases"> <img src="https://img.shields.io/github/v/release/Neocky/pluGET?include_prereleases" alt"latestrelease"></a>
<a href="https://github.com/Neocky/pluGET/releases"> <img src="https://img.shields.io/github/downloads/Neocky/pluGET/total" alt="downloads" border="0"></a>
<a href="https://discord.gg/475Uf4NBPF"><img src="https://discordapp.com/api/guilds/801903246284685312/widget.png?style=shield"/></a>
</p>

# 🚚💨 pluGET

A powerful package manager that updates plugins and server software for Minecraft servers.   

![pluget-27090b452c1e9](https://github.com/user-attachments/assets/9bfdafd8-2f89-4c00-96b3-05b78b0fdf71)


## 💡 About

pluGET is a standalone package manager written in Python for Minecraft servers running [Spigot](https://www.spigotmc.org/) and its forks like [PaperMC](https://papermc.io/).  
It works with locally installed servers or remote hosts via SFTP/FTP (configured in the config file).  
pluGET uses the APIs of [Spigot](https://www.spigotmc.org/), [Modrinth](https://modrinth.com/), and [GitHub](https://github.com/) to:
- Check plugin versions
- Download updates automatically
- Compare installed and latest versions
- Update supported server software (e.g. PaperMC)

Managing plugins is one of the most time-consuming parts of running a Minecraft server. Checking for updates manually and downloading each plugin takes a lot of time.
pluGET automates this process and makes plugin management simple and fast.

It is designed for server owners who want to save time and keep their plugins up to date. The configuration is simple, so even users without advanced technical knowledge can use it.


## 📖 Features

- Works locally or through SFTP/FTP
- Runs directly from the console with command line arguments
- Checks for updates and downloads the latest version of all/specific plugins
- **Multi-platform plugin support:**
  - [Spigot](https://www.spigotmc.org/) (via Spiget API)
  - [Modrinth](https://modrinth.com/) (with accurate file hash matching)
  - [GitHub](https://github.com/) releases (with name matching)
- Checks for updates and downloads the latest version of your server software
  - [PaperMc](https://papermc.io/)
  - [Purpur](https://purpurmc.org/)
  - [Waterfall](https://papermc.io/downloads#Waterfall)
  - [Velocity](https://papermc.io/downloads#Velocity)

There are more features in the work. Check [Projects](https://github.com/Neocky/pluGET/projects) for a complete list.  

**So why do it manually when you can use pluGET to automate it?** 🚀  
[Get the latest release here.](https://github.com/Neocky/pluGET/releases)  


## ☕ Support

If you enjoy using pluGET and would like to support its development, [you can buy me a hot chocolate](https://ko-fi.com/Y8Y1CKZ43). ☕🤎  
Your support helps keep the project active and maintained.


## ❓ Need help or have a question?

If you need help, have a question, or want to discuss something about pluGET, feel free to [join the Discord](https://discord.gg/475Uf4NBPF) or start a conversation in [GitHub Discussions](https://github.com/Neocky/pluGET/discussions).


## 💻 Installation

### 1. Requirements

- Python (Version 3.10+)
- (Recommended) [uv](https://docs.astral.sh/uv/)

```shell
python --version
```

If Python is not installed, download it from: https://www.python.org/downloads/

### 2. Download pluGET

[Download the latest release from GitHub.](https://github.com/Neocky/pluGET/releases)  
Unzip the archive and open a terminal in the extracted folder.

### 3. Setup

#### a. Recommended Setup (with [uv](https://docs.astral.sh/uv/))

Inside the pluGET folder un:

```shell
uv venv
uv sync
```

Then start the program with:

```shell
uv run python pluget.py
```

The dependencies are installed automatically.

#### b. Alternative Setup (without [uv](https://docs.astral.sh/uv/))

If you don't want to use uv:

##### Create a virtual environment:

```shell
python -m venv .venv
```

Activate it:

**Windows**

```powershell
.venv\Scripts\activate
```

**Linux**

```bash
source .venv/bin/activate
```

##### Install dependencies

```shell
pip install .
```

##### Start pluGET

```shell
# Windows:
py pluget.py
# Linux
python3 pluget.py
```

### 4. First Start (Config File)

On first launch, pluGET will create:

```shell
pluGET_config.yaml
```

The program will then exit.

1. Open the config file
2. Enter your server connection details
3. Start pluGET again

**Now you are good to go!**  


## 🚀 Usage and Commands

> [!Caution]
> As always, if you update plugins, shut down your server!  

### • Show the information about all commands:

<!-- <details>
  <summary>Output</summary>  
  
  ![Example output](https://i.ibb.co/9VZCjD6/pluget-help2.png)
  
</details> -->

```
help command [all/command]
```

### • Exit program:

```
exit .
```

### • Get link to this page:

```
help .
```

###  Manage Plugins

#### • Download the latest update of a specific package:

```
get [pluginID/pluginName]
```  

#### • Check all plugins/one specific plugin for updates with optional changelog output:

<!-- <details>
  <summary>Output</summary>  
  
  ![Output](https://i.ibb.co/VmSNh6K/pluget-checkall.png)
  
</details> -->

```
check [all/pluginName] [changelog]
```

#### • Update all plugins/one specific plugin:  
```
update [all/pluginName]
```  

#### • Remove a plugin with the ID/Name:  
```
remove [pluginID/pluginName]
```

#### • Search for a plugin:  
```
search [pluginName]
```

#### • Download plugin from GitHub releases:  
```
get-github [owner/repo]
```

#### • Download plugin from Modrinth:  
```
get-modrinth [project-id]
```

#### • Search for plugins on GitHub:  
```
search-github [searchTerm]
```

#### • Search for plugins on Modrinth:  
```
search-modrinth [searchTerm]
```

### Manage Server Software

#### • Check installed server software for updates:
```
check serverjar
```

#### • Update installed server software to latest/specific version:
```
update serverjar [Version]
```

#### • Download specific paper version:
```
get-paper [paperBuild] [minecraftVersion]
```

#### • Download specific waterfall version:
```
get-waterfall [waterfallBuild] [minecraftVersion]
```

#### • Download specific velocity version:
```
get-velocity [velocityBuild] [minecraftVersion]
```

#### • Download specific purpur version:
```
get-purpur [purpurBuild] [minecraftVersion]
```

## 🔩 Command line arguments

pluGET supports all commands directly through the command line.  
Get the list of all available command line arguments with the `-h` argument:

```shell
py pluget.py -h
```

Example direct command line call:

```shell
py pluget.py check all
```

## ⚙️ Developement

Contributions are very welcome!  
If you’d like to contribute, please read the
[Contributing Guidelines](CONTRIBUTING.md) first.  
Pull requests, bug reports, and feature suggestions are always appreciated.

### Development Setup

#### 1. Clone the repository

```shell
git clone https://github.com/Neocky/pluGET.git
cd pluGET
```

#### 2. Create a virtual environment and install dependencies

Using [uv](https://docs.astral.sh/uv/) (recommended):

```shell
uv venv
uv sync --extra dev
```

Without [uv](https://docs.astral.sh/uv/):

```shell
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .[dev]
```


## ⛔ Known problems

### Can't get latest version/Update available

#### Inconsistent Names and Versions

Example:
![EssentialsX](https://i.ibb.co/fDyCYQ8/essentialsx.png)  
EssentialsX is a prominent example of inconsisten version naming. The installed version is `2.18.2.0` but on [Spigot](https://www.spigotmc.org/resources/essentialsx.9089/update?update=371379) the version is only described as `2.18.2`.  
That's the reason pluGET can't detect it automatically.  
> There are of course many more plugins which have some sort of inconsistency which makes it sadly impossible for pluGET to detect them all. EssentialsX is used only as an example.  

#### Solution

Download the plugins with the `get [pluginName]` command to make them detectable for pluGET.  
After downloading EssentialsX with `get EssentialsX` and using `check all`:  
![EssentialsX](https://i.ibb.co/ws5wHTj/essentialsx-2.png)  
EssentialsX is now detected from pluGET and can update automatically when a new version comes out.  

### Bukkit plugins

Example:  
![worldguard](https://i.ibb.co/7NJ9HRG/pluget-checkallonlyone.png)  
As you can see the installed version was found but not the latest version for this plugin.  
This is because this is a plugin which is not available on [Spigot](https://www.spigotmc.org/resources/).
pluGET supports currently only plugins from [Spigot](https://www.spigotmc.org/resources/).  
In this example this is a bukkit plugin.  
