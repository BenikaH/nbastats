"""
miscellaneous helper functions
"""

from datetime import date
import os

# constants
ALL_TEAMS = [
    "ATL", "BOS", "BKN", "CHA", "CHI",
    "CLE", "DAL", "DEN", "DET", "GSW",
    "HOU", "IND", "LAC", "LAL", "MEM",
    "MIA", "MIL", "MIN", "NOP", "NYK",
    "OKC", "ORL", "PHI", "PHX", "POR",
    "SAC", "SAN", "TOR", "UTA", "WAS"
    ]

def convert_to_date(datestring):
    """
    returns date from a string with format
    datestring = 'yyyy-mm-dd'
    """
    year = int(datestring[:4])
    month = int(datestring[5:7])
    day = int(datestring[8:10])
    return date(year,month,day)

def find_playoff_series(year):
    # returns a list containing each playoff series
    # for the given year sorted by date of the first game
    # row format = [higher seed, lower seed, startdate, enddate]
    directory = '/home/kevin/Code/NBA/17-18/{}/'.format(year)
    matchups = set()
    series = []
    for f in os.listdir(directory):
        if '-0041' in f:
            game_date = convert_to_date(f[1:11])
            away = f[24:27]
            home = f[28:31]
            matchup = frozenset([away, home])
            if matchup in matchups:
                index = 0
                for i, x in enumerate(series):
                    if frozenset([x[0], x[1]]) == matchup:
                        if x[2] > game_date:
                            series[i][0] = home
                            series[i][1] = away
                            series[i][2] = game_date
                        if x[3] < game_date:
                            series[i][3] = game_date

            else:
                matchups.add(matchup)
                series.append([home, away, game_date, game_date])

    series.sort(key = lambda x: x[2])
    return series

def find_season_dates(year):
    # returns dict containing [startdate, enddate] for
    # 'regular' and 'playoffs'

    directory = '/home/kevin/Code/NBA/17-18/{}/'.format(year)
    x = [date(1000, 1, 1), date(1000, 1, 1)]
    dates = {
            'regular': [date(3000, 1, 1), date(100, 1, 1)],
            'playoffs': [date(3000, 1, 1), date(100, 1, 1)]
            }

    # get regular season and playoff dates
    for f in os.listdir(directory):
        if '-0021' in f:
            game_date = convert_to_date(f[1:11])
            if dates['regular'][0] > game_date:
                dates['regular'][0] = game_date
            if dates['regular'][1] < game_date:
                dates['regular'][1] = game_date
        elif '-0041' in f:
            game_date = convert_to_date(f[1:11])
            if dates['playoffs'][0] > game_date:
                dates['playoffs'][0] = game_date
            if dates['playoffs'][1] < game_date:
                dates['playoffs'][1] = game_date

    return dates
