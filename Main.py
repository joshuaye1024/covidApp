from tkinter import StringVar

import requests
import json
import pandas as pd


def getCovidData(date, region):
    """
    :param date:
    :param region:
    :return: Dictionary of Covid Data fields and values

    To grab historic data, use the string "daily" for the date parameter.
    """

    if (region == 'us'):
        url = "https://api.covidtracking.com/v1/us/" + date + ".json"
        if (date == 'current'):
            data = json.loads(requests.get(url).text)[0]
        elif (date == 'daily'):
            #create numpy array with columns as fields
            chunks = json.loads(requests.get(url).text)
            data = pd.DataFrame(chunks)
        else:
            data = json.loads(requests.get(url).text)
    else:
        url = "https://api.covidtracking.com/v1/states/" + region + "/" + date + ".json"
        if(date == 'daily'):
            chunks = json.loads(requests.get(url).text)
            data = pd.DataFrame(chunks)

        else:
            data = json.loads(requests.get(url).text)

    return data

def lowerStringVar(var):
    """Function to convert the text in a StringVar to lower case"""
    if isinstance(var, StringVar):
        var.set(var.get().lower())