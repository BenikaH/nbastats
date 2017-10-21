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

def find_gamefiles(dates, teams):
    """
    returns filenames for games between the dates
    with the given home and away teams

    dates = ['yyyy-mm-day', 'yyyy-mm-day']
    teampairs = [[gsw, cle], [mil, lac]] would get
    all games between the dates for gsw @ cle and mil @ lac.
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
            away = f[24:27]
            home = f[28:31]

            if [away, home] in teams and dates[0] <= game_date <= dates[1]:
                filenames.append(directory + f)

    return filenames


def summarize_game(filename):
    """
    Provides a human readable box score style summary 
    of a game.
    """
    home = filename[-7:-4]
    away = filename[-11:-8]
    game_df = pd.read_csv(filename)

    # here is where we print the summary
    print("\n" + away + ' at ' + home + ' on ' + game_df.date[0])
    print("\n" + away + ": " + str(game_df.away_score[game_df.shape[0] - 1]))
    print(home+ ": " + str(game_df.home_score[game_df.shape[0] - 1]))

    # print leaders in pts, rbs, assts, blocks
    print("\nLeaders")
    
    points = game_df[["team", "player", "points"]] \
            .groupby(["team", "player"]).sum()
    ptsleader = points["points"].idxmax()
    print("points:", str(int(points.points[ptsleader])), "-", \
            ptsleader[1], ptsleader[0])

    rebounds = game_df.loc[game_df.event_type == "rebound"] \
            [["player", "team"]]
    rebounds = rebounds.groupby(["team", "player"]).size()
    rbsleader = rebounds.idxmax()
    print("rebounds:", str(rebounds[rbsleader]), "-", rbsleader[1], \
            rbsleader[0])

    assists = game_df[["team", "assist"]].groupby(["team", "assist"]).size()
    astleader = assists.idxmax()
    print("assists:", str(assists[astleader]), "-", astleader[1], \
            astleader[0])

    blocks = game_df[["team", "block"]].groupby(["team", "block"]).size()
    blkleader = blocks.idxmax()
    temp = "blocks: " + str(blocks[blkleader]) + " - " +  blkleader[1]
    if blkleader[0] == home:
        print(temp, away)
    else:
        print(temp, home)

    steals = game_df[["team", "steal"]].groupby(["team", "steal"]).size()
    stlleader = steals.idxmax()
    temp = "steals: " + str(steals[stlleader]) + " - " +  stlleader[1]
    if stlleader[0] == home:
        print(temp, away, "\n")
    else:
        print(temp, home, "\n")




    # print team advanced stats, ortg, drtg, etc.





