from tkinter import StringVar

import requests
import json


def getCovidData(date, region):
    # date param in yyyymmdd
    # region param in standard state abbreviation



    if (region == 'us'):
        url = "https://api.covidtracking.com/v1/us/" + date + ".json"
        if (date == 'current'):
            data = json.loads(requests.get(url).text)[0]
        else:
            data = json.loads(requests.get(url).text)
    else:
        url = "https://api.covidtracking.com/v1/states/" + region + "/" + date + ".json"
        data = json.loads(requests.get(url).text)


    #for key in data:
        #print(key + ' : ' + str(data[key]))
    return data

def lowerStringVar(var):
    """Function to convert the text in a StringVar to lower case"""
    if isinstance(var, StringVar):
        var.set(var.get().lower())