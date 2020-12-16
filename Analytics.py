import Main
import statsmodels.api as sm



def OLSBase(categories, dateFrom, region, rollingAverageInDays, lagInDays):
    """
    Base function for OLS calculations.
    :param categories:
    :param dateFrom:
    :param region:
    :param rollingAverageInDays:
    :param lagInDays:
    :return: regressionResults object; regression statistics can be called from this object.
    """
    # note for reference: first element in categories list is ALWAYS taken as x in OLS calculation. The second element is always taken as y.
    # This, however, will not change the r^2 value.

    f = Main.formatDataFrame(categories, dateFrom, region)

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


def getRSquared(categories, dateFrom, region, rollingAverageInDays, lagInDays):
    """
    Getter function for the rsquared statistic
    :param categories:
    :param dateFrom:
    :param region:
    :param rollingAverageInDays:
    :param lagInDays:
    :return: float; the rsquared number
    """

    if not len(categories) == 2:
        print("The categories array must have a length of 2!")
        return
    else:
        ols = OLSBase(categories, dateFrom, region, rollingAverageInDays, lagInDays)
        return ols.rsquared


def getOLSSlope(categories, dateFrom, region, rollingAverageInDays, lagInDays):
    """
    Getter function for the slope statistic
    :param categories:
    :param dateFrom:
    :param region:
    :param rollingAverageInDays:
    :param lagInDays:
    :return: float; the slope
    """
    if not len(categories) == 2:
        print("The categories array must have a length of 2!")
        return
    else:
        ols = OLSBase(categories, dateFrom, region, rollingAverageInDays, lagInDays)
        return ols.params[1]