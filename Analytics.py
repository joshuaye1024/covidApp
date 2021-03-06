# -*- coding: utf-8 -*-
# 2020-12-22
# Josh Ye

import Main
import statsmodels.api as sm
import inspect
import sys
from datetime import datetime, date, timedelta

def categories(reg):
    today = datetime.today()
    yesterdayDate = date(today.year, today.month, today.day) - timedelta(days = 1)

    return Main.getCovidData(str(Main.convertDateToInt(yesterdayDate)),str(reg)).columns

# TODO: make checks so that the data always has more than two data points. Warn if less than 10. This occurs when the rollingAverage/lagInDays is greater than the difference between dateTo and dateFrom.
def OLSBase(categories, dateTo, region, rollingAverageInDays, lagInDays, dateFrom=None):
    """
    Base function for OLS calculations.
    :param categories:
    :param dateTo:
    :param region:
    :param rollingAverageInDays:
    :param lagInDays:
    :return: regressionResults object; regression statistics can be called from this object.
    """
    # note for reference: first element in categories list is ALWAYS taken as x in OLS calculation. The second element is always taken as y.
    # This, however, will not change the r^2 value.
    try:
        f = Main.formatDataFrame(categories, dateTo, region, dateFrom)
    except Exception as e:
        print(e)
        sys.exit(1)

    # shift x var by lagInDays.
    f[str(categories[0])] = f[str(categories[0])].shift(lagInDays)

    # get graphable columns

    cols = list(f.columns)

    for col in cols:
        if not col == 'date':
            f[col] = f[col].rolling(rollingAverageInDays).mean()

    # drop rows with NaN as the only values
    f = f.dropna()

    x = f[str(categories[0])]
    y = f[str(categories[1])]

    # we add constant here to make sure regression is in form y_i = ax_i + b
    ols = sm.OLS(y, sm.add_constant(x)).fit()

    return ols


def getRSquared(categories, dateTo, region, rollingAverageInDays, lagInDays, dateFrom=None):
    """
    Getter function for the rsquared statistic
    :param categories:
    :param dateTo:
    :param region:
    :param rollingAverageInDays:
    :param lagInDays:
    :return: float; the rsquared number
    """

    if not len(categories) == 2:
        print("The categories array must have a length of 2!")
        return
    else:
        ols = OLSBase(categories, dateTo, region, rollingAverageInDays, lagInDays, dateFrom)
        return ols.rsquared


def getOLSSlope(categories, dateTo, region, rollingAverageInDays, lagInDays, dateFrom=None):
    """
    Getter function for the slope statistic
    :param categories:
    :param dateTo:
    :param region:
    :param rollingAverageInDays:
    :param lagInDays:
    :return: float; the slope
    """
    if not len(categories) == 2:
        print("The categories array must have a length of 2!")
        return
    else:
        ols = OLSBase(categories, dateTo, region, rollingAverageInDays, lagInDays, dateFrom)
        return ols.params[1]