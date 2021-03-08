<p align="center">
<img src="https://i.ibb.co/JyCxnQn/logoreal.png" alt="pluGET" border="0"></a>
</p>

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
### Needed packages
Install the needed packages for this project.  
Execute this command in the ```/plugGET``` folder:  
```python
pip install -r requirements.txt
```

## Usage
Run programm.  
The following are examples for the general usage:  
(Hint: 'all' can always be exchanged through the plugin name or the plugin id and reverse)  
#### Download latest update of specific package:  
```
get 'pluginName'
```  
or:    
```
get 'pluginID'
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

