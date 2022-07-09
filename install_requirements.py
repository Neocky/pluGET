"""
    Install the needed python packages through this script
"""

import os

try:
    print("Installing Python packages and dependencies from requirements.txt...\n")
    os.system('py -m pip install -r requirements.txt' if os.name=='nt' else 'pip install -r requirements.txt')
    print("\nStart pluGET by launching the 'pluGET.py' file!")
except Exception as e:
    print(f"Requirements couldn't be installed.\nError message: {e}\n\nCommon solution: Check if file 'requirements.txt' is in the same folder and that Python3\
         and pip is installed!")
