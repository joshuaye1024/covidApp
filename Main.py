from tkinter import StringVar

import requests
import json
import pandas as pd

import matplotlib.pyplot as plt
from datetime import datetime


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


def graphCovidData(category, dateFrom, region,rollingAverageInDays):
    def convertIntToTime(number):
        datetime_object = datetime.strptime(str(number), '%Y%m%d')

        return datetime_object

    f = getCovidData("daily", region)

    # reverse data frame
    f = f.iloc[::-1].reset_index()

    # get index of target date
    index = int(f.loc[f['date'] == dateFrom].index[0])

    # return the data from start of covid to this date; show only graphable columns
    f = f.iloc[:index][['date', category]]

    f['date'] = f['date'].apply(lambda x: convertIntToTime(x))

    # get graphable columns

    f[category] = f[category].rolling(rollingAverageInDays).mean()

    # show the plot
    f.plot(x='date', y=category, kind='line')

    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)

    plt.show()