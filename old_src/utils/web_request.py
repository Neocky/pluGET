# Handles the web requests
import requests


def doAPIRequest(url):
    headers = {'user-agent': 'pluGET/1.0'}
    response = requests.get(url, headers=headers)
    packageDetails = response.json()
    return packageDetails
