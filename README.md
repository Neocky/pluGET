
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

A plugin manager that handles [Spigot plugins](https://www.spigotmc.org/resources/) for minecraft servers written in python.  

## Issues? Found a bug? 
[Create an issue.](https://github.com/Neocky/pluGET/issues/new/choose)  

## About  
This is a plugin manager for minecraft [Spigot](https://www.spigotmc.org/) servers and its forks (e.g. [PaperMC](https://papermc.io/)).  
It uses the [Spiget](https://spiget.org/) API to download and compare plugin versions.  
It can download the newest version of plugins.

## Installation
### Python
Python needs to be installed on your machine.  
Get it [here](https://www.python.org/downloads/).  
### Dependencies
Install the needed packages for this project.  
Execute this command in the ```/plugGET``` folder:  
```python
pip install -r requirements.txt
```

### Edit the Config
When run the first time, the config will be created in the root package folder and the program will close.  
Edit the config to your needs and rerun it.  
**Now you are good to go!**  

## Usage  
The following are examples for the general usage:  
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
