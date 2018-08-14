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

TEAM_COLORS = {
        'ATL': ['#cc092f', '#ffffff'],
        'BOS': ['#008853', '#bca9a5c', '#aa4641', '#2a3236'],
        'BKN': ['#000000', '#ffffff'],
        'CHA': ['#1d8cab', '#1d0c65'],
        'CHI': ['#bc032b', '#000000'],
        'CLE': ['#860038', '#002b60', '#fdbb30'],
        'DAL': ['#1061ac', '#c4ced4', '#000000'],
        'DEN': ['#fdb827', '#4b90cd', '#002d62'],
        'DET': ['#ed174c', '#0067b1', '#002d62'],
        'GSW': ['#006bb6', '#fdb927'],
        'HOU': ['#d31145', '#061922'],
        'IND': ['#002d62', '#ffc526', '#bec0c2'],
        'LAC': ['#d81d47', '#0061a1', '#1a1919'],
        'LAL': ['#fdb827', '#542583'],
        'MEM': ['#23375b', '#6189b9', '#fbb829'],
        'MIA': ['#bf2f38', '#f59814', '#061922'],
        'MIL': ['#00461b', '#efebd2'],
        'MIN': ['#005183', '#0ea94e', '#a8aaad', '#010101'],
        'NOP': ['#002a5c', '#b5985a', '#e51937'],
        'NYK': ['#f48328', '#046ab4', '#bcbec4'],
        'OKC': ['#1e3160', '#f05333', '#0a7ec2', '#fcbb30'],
        'ORL': ['#0075bd', '#c6cdd3', '#071922'],
        'PHI': ['#003da5', '#d50032'],
        'PHX': ['#27235c', '#faa120', '#5b6770', '#e66226'],
        'POR': ['#e13a3e', '#c4ced4', '#000000'],
        'SAC': ['#724c9f', '#909291', '#000000'],
        'SAN': ['#84888b', '#000000'],
        'TOR': ['#be0f34', '#a8a9ab', '#000000'],
        'UTA': ['#0c2340', '#f9a01b', '#00471b'],
        'WAS': ['#e51837', '#002a5c', '#919191'],
        }

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
