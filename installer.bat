@ECHO OFF

cd /d %~dp0

Echo          ___           ___       ___           ___           ___           ___     
Echo         /\  \         /\__\     /\__\         /\  \         /\  \         /\  \    
Echo        /::\  \       /:/  /    /:/  /        /::\  \       /::\  \        \:\  \   
Echo       /:/\:\  \     /:/  /    /:/  /        /:/\:\  \     /:/\:\  \        \:\  \  
Echo      /::\~\:\  \   /:/  /    /:/  /  ___   /:/  \:\  \   /::\~\:\  \       /::\  \ 
Echo     /:/\:\ \:\__\ /:/__/    /:/__/  /\__\ /:/__/_\:\__\ /:/\:\ \:\__\     /:/\:\__\
Echo     \/__\:\/:/  / \:\  \    \:\  \ /:/  / \:\  /\ \/__/ \:\~\:\ \/__/    /:/  \/__/
Echo          \::/  /   \:\  \    \:\  /:/  /   \:\ \:\__\    \:\ \:\__\     /:/  /     
Echo           \/__/     \:\  \    \:\/:/  /     \:\/:/  /     \:\ \/__/     \/__/      
Echo                      \:\__\    \::/  /       \::/  /       \:\__\                  
Echo                       \/__/     \/__/         \/__/         \/__/                  
Echo `
Echo `
Echo                        ------------------------------------
Echo                                     [By Neocky]
Echo                          https://github.com/Neocky/pluGET
Echo                                   pluGET-Installer
Echo                        ------------------------------------
Echo `
Echo     ----------------------------------------------------------------------------------
Echo [93mInstalling Python packages and dependencies...[0m

py -m pip install -r requirements.txt

Echo `
Echo [92mLaunching pluGET...[0m

launcher.bat

exit
