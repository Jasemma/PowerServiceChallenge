"""
Module that contains the get trades functionality. This module will generate a random set of dummy positions.
"""
import random
import logging
import datetime
import uuid

import numpy as np
import pandas as pd

#from datetime import datetime, timedelta


def check_if_valid_date(date: str):
    """
    Verify that the date format matches d/m/y
    :param date: str date in d/m/y format
    :return: True or False
    """
    date_format = "%d/%m/%Y"

    """ Warning to any non python devs reading this code..
        In Python the only way to test a valid date is with a try catch. Yep, it sux.
    """
    if not isinstance(date, str):
        return False

    try:
        datetime.datetime.strptime(date, date_format)
        valid_date = True
    except ValueError:
        valid_date = False

    return valid_date

def random_nan(x):
    """
    Replace x with a nan, if the random number == 1
    """
    if random.randrange(0, 15) == 1:
        x = np.nan

    return x


def generate_new_random_trade_position(date: str):
    """ Generates a new random trade position with the date, period sequence and volume sequence
    :param date: Date in d/m/y format
    :return: dict with data
    """

    period_list = [random_nan(i.strftime("%H:%M")) for i in pd.date_range("00:00", "22:59", freq="5min").time]
    volume = [random_nan(x) for x in random.sample(range(0, 500), len(period_list))]

    open_trade_position = {"date": date,
                           "time": period_list,
                           "volume": volume,
                           "id": uuid.uuid4().hex
                           }

    return open_trade_position


def get_trades(date: str):
    """
    Generate some random number of open trade positions
    :param date: date in d/m/y format
    :return:
    """

    if not check_if_valid_date(date=date):
        error_msg = "The supplied date {} is invalid.Please supply a date in the format d/m/Y.".format(date)
        logging.error(error_msg)
        raise ValueError(error_msg)

    # a randomly chosen number of open trades
    number_of_open_trades = random.randint(1, 101)
    logging.info("Generated" + str(number_of_open_trades) + " open trades randomly.")

    open_trades_list = []
    # Generate a list of open trade dicts
    for open_trade in range(0, number_of_open_trades):
        open_trades_list.append(generate_new_random_trade_position(date=date))

    return open_trades_list


if __name__ == '__main__':
    trades = get_trades(date='11/09/2022')
    df = pd.DataFrame(trades[0]).assign(date=lambda df: pd.to_timedelta(df.date.str.split().str[1])).groupby(pd.Grouper(key='time', axis=0, freq='H')).sum('volume')
    #df['time'] = pd.to_timedelta(df['time'].date.str.split().str[1])
    #grouped = df.groupby(pd.Grouper(key='time', axis=0, freq='H')).sum('volume')
    #outcome = grouped.set_index(['hourly', 'volume'])
    print(df)





    #today_date = datetime.date.today()
    #bftrades = get_trades(today_date)



    #df['seconds'] = df['time'].dt.time
    #df['hour'] = pd.to_timedelta(df['seconds'])
    #df.groupby([df.dt.hour, df.dt.minute])['volume'].sum()
    
    #df1 = time.resample('60min').first()
    
    # df1 = df.groupby('time').sum()
    
    #df['time'] = df['time'].datetime.datetime.strftime('%H:%M')
    #df1 = df.groupby('time')['volume'].sum()
    #df2 = pd.to_timedelta(df1['time'])
    #df2 = time.set_index(['date','time','volume','id'])