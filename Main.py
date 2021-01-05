# -*- coding: utf-8 -*-
# 2020-12-22
# Josh Ye

from tkinter import StringVar

import requests
import json
import pandas as pd

import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
import inspect
from matplotlib.widgets import Slider

def getCovidData(date, region):
    """
    :param date: int
    :param region: string
    :return: Dictionary of Covid Data fields and values

    To grab historic data, use the string "daily" for the date parameter.
    """

    if (region == 'us'):
        url = "https://api.covidtracking.com/v1/us/" + date + ".json"
        date = str(date)
        if (date == 'current'):
            data = json.loads(requests.get(url).text)[0]
        elif (date == 'daily'):
            # create numpy array with columns as fields
            chunks = json.loads(requests.get(url).text)
            data = pd.DataFrame(chunks)
        else:
            data = json.loads(requests.get(url).text)
    else:
        url = "https://api.covidtracking.com/v1/states/" + region + "/" + date + ".json"
        if (date == 'daily'):
            chunks = json.loads(requests.get(url).text)
            data = pd.DataFrame(chunks)

        else:
            data = json.loads(requests.get(url).text)

    return data


def lowerStringVar(var):
    """Function to convert the text in a StringVar to lower case"""
    if isinstance(var, StringVar):
        var.set(var.get().lower())


def convertIntToDate(number):
    """
    Converts dateInt to date for server write
    :param number: date in YYYYMMDD form to convert
    :return: equivalent date object of input date
    """
    dt = datetime.strptime(str(number), '%Y%m%d')

    date_object = date(dt.year, dt.month, dt.day)

    return date_object

def convertDateToInt(dt):
    """
    Converts date from server to dateInt input
    :param dt:
    :return: equivalent dateInt object; if input is not a date, return None.
    """
    #checks if input date is a date
    if isinstance(dt, date) == False:
        return None

    else:
        dateInt = int(dt.strftime('%Y%m%d'))

        return dateInt


def formatDataFrame(categories, dateTo, region, dateFrom=None):
    """
    :param categories: array of numerical categories to be processed
    :param dateFrom: int of date to grab data up to
    :region: string of region code
    :rollingAverageInDays: int of rolling average length
    :returns: dataframe of data
    """
    try:
        today = datetime.today()
        todayDate = date(today.year, today.month, today.day)

        if convertIntToDate(dateTo) == todayDate:
            #if dateTo is equal to the current date, use yesterday's dateInt as the dateTo param
            dateTo = convertDateToInt(todayDate - timedelta(days = 1))

        print(dateTo)

        f = getCovidData("daily", region)

        # reverse data frame
        f = f.iloc[::-1].reset_index()

        # get index of target date
        if not dateFrom == None:
            indexFrom = int(f.loc[f['date'] == dateFrom].index[0])
        indexTo = int(f.loc[f['date'] == dateTo].index[0])

        # return the data from start of covid to this date; show only graphable columns

        categories.append('date')
        categories = categories[::-1]

        #check whether dateFrom parameter is used; adjust accordingly
        if not dateFrom == None:
            if 'all' not in categories:
                f = f.iloc[indexFrom:indexTo][categories]
            else:
                f = f.iloc[indexFrom:indexTo]
        else:
            if 'all' not in categories:
                f = f.iloc[:indexTo][categories]
            else:
                f = f.iloc[:indexTo]
        print(type(f['date'][0]))

        f['date'] = f['date'].apply(lambda x: convertIntToDate(x))

        print(type(f['date'][0]))

        #replace all nan with 0
        f = f.fillna(0)

        return f

    except KeyError as ke:
        print("One or more of the parameters in the list of categories is invalid. Check and correct the parameters, then run again.")
        print('\033[91m' + "KeyError: " + str(ke))

    except IndexError as ie:
        print("The date is not inputted correctly. Check that the date is an integer in YYYYMMDD format and is not the current day.")
        print('\033[91m' + "KeyError: " + str(ie))

    except ValueError as ve:
        print("The region inputted is invalid. Correct the region code, then try again.")
        print('\033[91m' + "KeyError: " + str(ve))

def graphCovidData(categories, dateTo, region, rollingAverageInDays, windowTitle, dateFrom=None):
    """
    Returns a graph of the requested covid data.
    :param categories: array of numerical categories to be graphed
    :param categories: array of numerical categories to be graphed
    :param dateTo: int of date to be graphed up to
    :region: string of region code
    :rollingAverageInDays: int of rolling average length
    :windowTitle: string that defines the plot window's title
    :returns: graph of data
    """

    f = formatDataFrame(categories, dateTo, region, dateFrom)

    # get graphable columns

    cols = list(f.columns)

    # create common axis object
    ax = plt.gca()

    for col in cols:
        if not col == 'date':
            f[col] = f[col].rolling(rollingAverageInDays).mean()
            f.plot(x='date', y=col, kind='line', ax=ax)

    # show the plot

    # get current figure and set dimensions
    fig = plt.gcf()
    fig.canvas.set_window_title(windowTitle)
    fig.set_size_inches(10,6)

    plt.show()