"""
Module for stats from a single game.
"""

from datetime import date
import numpy as np
import pandas as pd
import os

def convert_to_date(datestring):
    """
    returns date from a string with format
    datestring = 'yyyy-mm-yy'
    """
    year = int(datestring[:4])
    month = int(datestring[5:7])
    day = int(datestring[8:10])
    return date(year,month,day)

def find_gamefiles(dates, home, away):
    """
    returns filenames for games between the dates
    with the given home and away teams

    dates = ['yyyy-mm-day', 'yyyy-mm-day']
    home = list of 3 letter team codes
    away = list of 3 letter team codes
    """

    filenames = []

    dates[0] = convert_to_date(dates[0])
    dates[1] = convert_to_date(dates[1])

    # folder is only the ending year of the season
    if dates[0].month > 9:
        year0 = dates[0].year + 1
    else:
        year0 = dates[0].year
    if dates[1].month > 9:
        year1 = dates[1].year + 1
    else:
        year1 = dates[1].year

    # get relevant games in each folder
    for year in range(year0, year1 + 1):
        directory='/home/kevin/Code/NBA/17-18/{}/'.format(year)
        for f in os.listdir(directory):
            try:
                game_date = convert_to_date(f[1:11])
            except:
                game_date = date(1000, 1, 1)
            awayteam = f[24:27].lower()
            hometeam = f[28:31].lower()

            if hometeam in home and awayteam in away and \
                dates[0] <= game_date <= dates[1]:
                    filenames.append(f)

    return filenames




