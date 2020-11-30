import requests
import json


def getCovidData(date, region):
    # date param in yyyymmdd
    # region param in standard state abbreviation

    if (region == 'us'):
        url = "https://api.covidtracking.com/v1/us/" + date + ".json"
        data = json.loads(requests.get(url).text)[0]
    else:
        url = "https://api.covidtracking.com/v1/states/" + region + "/" + date + ".json"
        data = json.loads(requests.get(url).text)

    for key in data:
        print(key + ' : ' + str(data[key]))



getCovidData('current', 'ca')