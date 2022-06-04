"""
	Install the needed python packages through this script
"""

import os

try:
	print("Installing Python packages and dependencies from requirements.txt...")
	os.system('py -m pip install -r requirements.txt' if os.name=='nt' else 'pip install -r requirements.txt')
except:
	print("Requirements couldn't be installed. Check if file 'requirements.txt' is in the same folder and that Python3\
		 and pip is installed!")
