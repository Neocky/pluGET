
<p align="center">
<img src="https://i.ibb.co/JyCxnQn/logoreal.png" alt="pluGET" border="0"></a>
</p>

<p align="center">  
<a href="https://www.python.org/"> <img src="https://forthebadge.com/images/badges/made-with-python.svg" alt="madewithpython" border="0"></a>
</p>

<p align="center">  
<a href="https://github.com/Neocky/pluGET/blob/main/LICENSE"> <img src="https://img.shields.io/badge/license-Apache--2.0-blue" alt="Apache-2.0" border="0"></a>
<a href="https://github.com/Neocky/pluGET/stargazers"> <img src="https://img.shields.io/github/stars/Neocky/pluGET?color=yellow" alt="stars" border="0"></a>
<a href="https://github.com/Neocky/pluGET/releases"> <img src="https://img.shields.io/github/downloads/Neocky/pluGET/total" alt="downloads" border="0"></a>

</p>

# pluGET

A package manager that handles [Spigot plugins](https://www.spigotmc.org/resources/) for minecraft servers written in python.   


## Issues? Found a bug? 
[Create an issue.](https://github.com/Neocky/pluGET/issues/new/choose) 


## About  
This is a package manager for minecraft [Spigot](https://www.spigotmc.org/) servers and its forks (e.g. [PaperMC](https://papermc.io/)).  
Plugin management was the hard part of mangaging a minecraft server. The time i needed to check the [Spigot ressource](https://www.spigotmc.org/resources/) page for updates for the installed plugins was shocking.  
So I built pluGET to automate/ease the plugin handling for a minecraft server and to turn the shocking part of managing a minecraft server to an easy one.  
This program is suited for minecraft server owners who want to save time and stay on top of their plugin versions.  
The program input and the associated config file are pretty clear so every server owner and not only the most tech savy ones can use pluGET to ease their plugin handling.  
Follow the [Installation](https://github.com/Neocky/pluGET#installation) guide below for an easy and hassle free setup of pluGET.  
If you still have questions [here](https://github.com/Neocky/pluGET#need-help) is the best place to ask for support.

The program works with a locally installed server or with a remote host through SFTP, when configured in the config.
It uses the [Spiget](https://spiget.org/) API to download and compare plugin versions and can download the latest version of plugins from the [Spigot](https://www.spigotmc.org/) site.  
So what can it do exactly?  
pluGET can:
- work locally or through sftp
- download the latest version of a plugin
- update every installed/one specific plugin
- check for an update of every installed/one specific plugin
- remove a plugin from the plugin folder


## Need help?
[<img src="https://i.imgur.com/D5vyVzC.png" alt="Discord" width="400"/>](https://discord.gg/475Uf4NBPF)


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
When run the first time, the config will be created in the root package folder and the program will close.  
Edit the config to your needs and relaunch pluGET.  
**Now you are good to go!**  


## Usage  
Execute the launcher.bat in the ```\pluGET``` folder. This will launch pluGET correctly.  
The following are examples of input for the general usage:  
(Hint: 'all' can always be exchanged through the plugin name or the plugin id and reverse)  
#### Download the latest update of a specific package:  
```
get 'pluginID'
```  
or:    
```
get 'pluginName'
```  
#### Check all installed plugins for updates:  
```
check all
```  
#### Check one plugin for updates:
```
check 'pluginName'
```  
#### Update all installed plugins:  
```
update all
```  
#### Update only one plugin:  
```
update 'pluginName'
```  
#### Exit program:
```
exit .
```
#### Get link to here:
```
help .
```
