import requests
import json

zip2fips = json.load(open('/home/davidseo901/project/zip2fips/zip2fips.json'))

def coordinateToFips(lat, lon):
    url = 'https://geo.fcc.gov/api/census/block/find?latitude=' + str(lat) + '&longitude=' + str(lon) + '&format=json'
    response = requests.get(url)
    data = response.json()
    if "County" not in data:
        return 0
    else:
        return int(data["County"]["FIPS"])

def zipToFips(zip):
    zipstr = str(zip)
    if zipstr not in zip2fips:
        return 0
    else:
        return int(zip2fips[zipstr])
