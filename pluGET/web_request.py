import requests
#import urllib.request


def doAPIRequest(url):
    headers = {'user-agent': 'pluGET'}
    response = requests.get(url, headers=headers)
    packageDetails = response.json()
    return packageDetails
