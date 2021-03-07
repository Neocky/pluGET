# Handles the web requests
import requests
import cloudscraper
#import urllib.request


def doAPIRequest(url):
    headers = {'user-agent': 'pluGET'}
    response = requests.get(url, headers=headers)
    packageDetails = response.json()
    return packageDetails

def createCloudScraperInstance():
    global CLOUDSCRAPER
    CLOUDSCRAPER = cloudscraper.create_scraper()  # returns a CloudScraper instance
    return CLOUDSCRAPER