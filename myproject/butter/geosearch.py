import requests
import json

zip2fips = json.load(open('/home/davidseo901/project/zip2fips/zip2fips.json'))

def coordinateToFips(lat, lon):
    url = 'https://geo.fcc.gov/api/census/block/find?latitude=' + str(lat) + '&longitude=' + str(lon) + '&format=json'
    response = requests.get(url)
    data = response.json()
    return int(data["County"]["FIPS"])

def zipToFips(zip):
    zipstr = str(zip)
    return int(zip2fips[zipstr])
