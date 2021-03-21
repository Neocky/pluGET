

<p align="center">
<img src="https://i.ibb.co/JyCxnQn/logoreal.png" alt="pluGET" border="0"></a>
</p>

<p align="center">  
<a href="https://www.python.org/"> <img src="https://forthebadge.com/images/badges/made-with-python.svg" alt="madewithpython" border="0"></a>
</p>

<p align="center">  
<a href="https://github.com/Neocky/pluGET/blob/main/LICENSE"> <img src="https://img.shields.io/github/license/Neocky/pluGET" alt="Apache-2.0" border="0"></a>  
<a href="https://github.com/Neocky/pluGET/releases"> <img src="https://img.shields.io/github/v/release/Neocky/pluGET?include_prereleases" alt"latestrelease"></a>
<a href="https://github.com/Neocky/pluGET/releases"> <img src="https://img.shields.io/github/downloads/Neocky/pluGET/total" alt="downloads" border="0"></a>
<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FNeocky%2FpluGET&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false"/></a>


</p>


# pluGET  
#### A powerfull package manager which handles [Plugins](https://www.spigotmc.org/resources/) and Server Software for minecraft servers.   

<img src="https://i.ibb.co/82dnyrK/image.png" alt="meme" border="0" height="350" width="350"></a>



## Issues? Found a bug? 
[Create an issue.](https://github.com/Neocky/pluGET/issues/new/choose) 


## About  
This is a package manager for minecraft [Spigot](https://www.spigotmc.org/) servers and its forks (e.g. [PaperMC](https://papermc.io/)).  
This is a standalone program written in python.  
The program works with a locally installed server or with a remote host through SFTP, when configured in the config.  
It uses the [Spiget](https://spiget.org/) API to download and compare plugin versions and can download the latest version of plugins from the [Spigot](https://www.spigotmc.org/) site.  
It can also compare and download the latest update of specifif server software (e.g. [PaperMC](https://papermc.io/)).  

Plugin management was the hard part of mangaging a minecraft server. The time it took to check the [Spigot ressource](https://www.spigotmc.org/resources/) page for updates for the installed plugins and updating all plugins manually which have available updates was too long and shocking.  
So I built pluGET to automate and ease the plugin handling of a minecraft server and to turn the most time consuming part of managing a minecraft server to an easy one.  

This program is suited for minecraft server owners who want to save time and stay on top of their plugin versions.  
The program input and the associated config file are pretty simple so every server owner and not only the most tech savy ones can use pluGET to ease their plugin handling.  

Follow the [Installation](https://github.com/Neocky/pluGET#installation) guide below for an easy and hassle free setup of pluGET.  
Read [Usage](https://github.com/Neocky/pluGET#usage) below to get some example inputs when using pluGET.  
If you still have questions [here](https://github.com/Neocky/pluGET#need-help) is the best place to ask for support.  

So what can it do exactly?  
pluGET can:
- work locally or through sftp
- manage plugins:
  - download the latest version of a plugin
  - update every installed/one specific plugin
  - check for an update of every installed/one specific plugin
  - remove a plugin from the plugin folder
- manager server software:
  - download a specific server software version
  - check instlalled server software for update
  - update installed server software to a specific version
  - supported server software: [PaperMc](https://papermc.io/)

There are more features in the work. Check [Projects](https://github.com/Neocky/pluGET/projects) for a complete list.  

**So why do it manually when you can use pluGET to automate it?** 🚀  
[Get the latest release here.](https://github.com/Neocky/pluGET/releases)  


## Donations
If you feel like showing your love and/or appreciation for this project then how about buying me a coffee! :)  
  
<a href="https://www.buymeacoffee.com/Neocky" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="76" width="272"></a>


## Need help?
[<img src="https://i.imgur.com/D5vyVzC.png" alt="Discord" width="272"/>](https://discord.gg/475Uf4NBPF)


## Installation
### Python
Python needs to be installed on your machine.  
Get it [here](https://www.python.org/downloads/).  
### Dependencies
Install the needed packages for this project.  
Execute this command in the ```\plugGET``` folder:  
```python
pip install -r requirements.txt
```


### Edit the Config
When run the first time, the `config.ini` file will be created in the root package folder and the program will close.  
Edit the config to your needs and relaunch pluGET.  
**Now you are good to go!**  


## Usage  
> As always, if you update plugins, shut down your server!  

Execute the `launcher.bat` in the `\pluGET` folder. This will launch pluGET correctly.  
Another way is to launch the `src\__main__.py` file.  
The following are examples of input for the general usage:  
(Hint: [thingsInBrackets] are optional & 'all' can always be exchanged through the plugin name or the plugin id and reverse) 

### General
#### Command help:
`help command [all/command]`  
```
help command
```
<details>
  <summary>Output</summary>  
  
  ![Output](https://i.ibb.co/9VZCjD6/pluget-help2.png)
  
</details>

### Manage Plugins
#### Download the latest update of a specific package: 
`get [pluginID/pluginName]`  
```
get 'pluginID'
```  
or:    
```
get 'pluginName'
```  
#### Check all plugins/one specific plugin for updates:  
`check [all/pluginName]`  
```
check all
```  
or:  
```
check 'pluginName'
```  

<details>
  <summary>Output</summary>  
  
  ![Output](https://i.ibb.co/VmSNh6K/pluget-checkall.png)
  
</details>


#### Update all plugins/one specific plugin:  
`update [all/pluginName]`  
```
update all
```  
or:  
```
update 'pluginName'
```  
#### Remove a plugin with the ID/Name:  
`remove [pluginID/pluginName]`
```
remove 'pluginID'
```  
or:  
```
remove 'pluginName'
```  
#### Search for a plugin:  
`search [pluginName]`  
```
search 'pluginName'
```
#### Exit program:
`exit [anything]`  
```
exit .
```
#### Get link to here:
`help [anything]`  
```
help .
```
### Manage Server Software
#### Check installed server software for updates:
`check serverjar`  
```
check serverjar
```
### Update installed server software to latest/specific version:
`update serverjar [Version]`  
```
update serverjar 'PaperMCVersion'
```
### Download specific paper version:
`get-paper [paperBuild] [minecraftVersion]`
```
get-paper 550 1.16.5
```
or:
```
get-paper 321
```

## Known problems

### Can't get latest version/Update available
For example:  
![worldguard](https://i.ibb.co/7NJ9HRG/pluget-checkallonlyone.png)  
As you can see the installed version was found but not the latest version for this plugin.  
This is because this is a plugin which is not available on [Spigot](https://www.spigotmc.org/resources/).
pluGET supports currently only plugins from [Spigot](https://www.spigotmc.org/resources/).  
In this example this is a bukkit plugin.  

