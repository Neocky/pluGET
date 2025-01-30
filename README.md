
<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/branding/pluget-logo-white.png">
  <source media="(prefers-color-scheme: light)" srcset="./assets/branding/pluget-logo-black.png">
  <img src="./assets/branding/pluget-logo-black.png" alt="pluGET" border="0">
</picture>
</p>

<p align="center">  
<a href="https://www.python.org/"> <img src="https://img.shields.io/badge/made%20with-python%20%F0%9F%90%8D-brightgreen" alt="madewithpython" border="0"></a>
</p>

<p align="center">  
<a href="https://github.com/Neocky/pluGET/releases"> <img src="https://img.shields.io/github/v/release/Neocky/pluGET?include_prereleases" alt"latestrelease"></a>
<a href="https://github.com/Neocky/pluGET/releases"> <img src="https://img.shields.io/github/downloads/Neocky/pluGET/total" alt="downloads" border="0"></a>
<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FNeocky%2FpluGET&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false"/></a>
<a href="https://discord.gg/475Uf4NBPF"><img src="https://discordapp.com/api/guilds/801903246284685312/widget.png?style=shield"/></a>
</p>


# 🚚💨 pluGET  
A powerful package manager which updates [Plugins](https://www.spigotmc.org/resources/) and Server Software for minecraft servers.   

<img src="https://user-images.githubusercontent.com/13088544/177011216-1360d444-278a-475e-9863-966c48c60ba7.gif" alt="pluGET.gif" border="0" />

<details>
  <summary>Old Screenshots</summary>  
  
  `check all` to check installed plugins for updates:  
  ![screenshot1](https://i.ibb.co/QM7xh7w/pluget-checkall-small.png)
  
  `check all` with more plugins:  
  ![screenshot2](https://i.ibb.co/VmSNh6K/pluget-checkall.png)
  
  `help command` list all available commands:  
  ![screenshot3](https://i.ibb.co/9VZCjD6/pluget-help2.png)
  
</details>

## 💡 About  
pluGET is a standalone package manager written in python for minecraft [Spigot](https://www.spigotmc.org/) servers and its forks (e.g. [PaperMC](https://papermc.io/)). The program works with a locally installed servers or with a remote host through SFTP/FTP, when configured in the config. It uses the [Spiget](https://spiget.org/) API to download and compare plugin versions and download the latest version of plugins from the [Spigot](https://www.spigotmc.org/) site. It can also compare and download the latest update of specific server software (e.g. [PaperMC](https://papermc.io/)).

Plugin management is the hard part of managing a minecraft server. The time it takes to manually check the [Spigot resources](https://www.spigotmc.org/resources/) page for updates and manually downloading all plugins is too long and daunting. So I built pluGET to automate and ease the plugin handling of a minecraft server and to turn the most time consuming part of managing a minecraft server to an easy one.

This program is suited for minecraft server owners who want to save time and stay on top of their plugin versions. The program input and the associated config file are pretty simple so every server owner and not only the most tech savy ones can use pluGET to ease their plugin handling.

<img src="https://i.ibb.co/82dnyrK/image.png" alt="meme" border="0" height="350" width="350"></a>

## 📖 Features
- Works locally or through SFTP/FTP
- Runs directly from the console with command line arguments
- Checks for updates and downloads the latest version of all/specific plugins
- Checks for updates and downloads the latest version of your server software
  - [PaperMc](https://papermc.io/)
  - [Purpur](https://purpurmc.org/)
  - [Waterfall](https://papermc.io/downloads#Waterfall)
  - [Velocity](https://papermc.io/downloads#Velocity)

There are more features in the work. Check [Projects](https://github.com/Neocky/pluGET/projects) for a complete list.  

**So why do it manually when you can use pluGET to automate it?** 🚀  
[Get the latest release here.](https://github.com/Neocky/pluGET/releases)  


## ☕ Support
If you feel like showing your love and/or appreciation for this project then how about buying me a coffee? ☕🤎

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y1CKZ43)

## ❓ Need help?
Check out the discord!

[<img src="https://i.ibb.co/PQv3KtJ/Discord-Logo-Wordmark-Color.png" alt="Discord" width="300"/>](https://discord.gg/475Uf4NBPF)


## 💻 Installation
### 1. Python 3.10.4
Python needs to be installed on your machine. Get it [here](https://www.python.org/downloads/).  

### 2. Dependencies
In order to install dependencies run the `install_requirements_WINDOWS/LINUX` file, of course depending on your system.

### 3. Edit the config
When run pluGET for the first time, the `pluGET_config.yaml` file will be created in the main folder and the program will close.  
Edit the config to your needs and relaunch pluGET.  
**Now you are good to go!**  

### 4. Running the program
Execute the `pluget.py` file with python in the `\pluGET` folder.  
This will launch pluGET correctly.  
```python
# Windows:
py pluget.py
# Linux
python3 pluget.py
```

## 🚀 Usage and Commands
> As always, if you update plugins, shut down your server!  

### • Show the information about all commands.
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

## ✅ Command line arguments
pluGET supports all commands directly through the command line. Get the list of all available command line arguments with the `-h` argument.

Example direct command line call:
```shell
py pluget.py check all
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
