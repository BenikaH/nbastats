"""
Module for stats from a single game.
"""

from datetime import date
from misc import convert_to_date
import numpy as np
import pandas as pd
import re
import os

def convert_time(timestring):
    """
    timestring = '00:00:00'
    """
    if float(timestring[:2]) > 0 or len(timestring) != 8:
        timestring = '00:00:00'
    return float(timestring[3:5])+float(timestring[6:])/60

def get_teams_date_from_file(gamefile):
    """
    assumes the file name also has the directory on it.
    probably should parse with regex...
    """
    hometeam = gamefile[-7:-4]
    awayteam = gamefile[-11:-8]
    date = convert_to_date(gamefile[-34:-24])
    return hometeam, awayteam, date

def find_gamefiles(dates, teams):
    """
    returns filenames for games between the dates
    with the given home and away teams

    dates = ['yyyy-mm-day', 'yyyy-mm-day']
    teampairs = [[GSW, CLE], [MIL, LAC]] would get
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

def get_lineup_stats(team, players, gamefiles, return_raw = False, \
        whole_team = False):
    """
    team = three letter team code (caps)
    players = list of at least five players to get stats for
    gamefiles = list of gamefiles
    return_raw = True will not just give the counting stats,
        not per 100

    returns stats, opp_stats
    which are the per 100 possession stats in the form
    note that possessions are estimated, not actual
    0 - poss
    1 - min
    2 - fg
    3 - fga
    4 - fg%
    5 - 3p
    6 - 3pa
    7 - 3p%
    8 - 2p
    9 - 2pa
    10 - 2p%
    11 - ft
    12 - fta
    13 - ft%
    14 - drb
    15 - orb
    16 - ast
    17 - stl
    18 - blk
    19 - tov
    20 - pf
    21 - pts = ortg
    22 - pts allowed = drtg
    23 - ts%
    24 - efg%
    25 - to%
    26 - orb%
    27 - ftr
    """
    # raw counting stats for self and opponents
    # 0 - fg
    # 1 - fga
    # 2 - 3p
    # 3 - 3pa
    # 4 - 2p
    # 5 - 2pa
    # 6 - ft
    # 7 - fta
    # 8 - drb
    # 9 - orb
    # 10 - ast
    # 11 - stl
    # 12 - blk
    # 13 - tov
    # 14 - foul (personal and technical)
    # 15 - pts
    raw_stats = {
            'fg': 0,
            'fga': 0,
            '3p': 0,
            '3pa': 0,
            '2p': 0,
            '2pa': 0,
            'ft': 0,
            'fta': 0,
            'drb': 0,
            'orb': 0,
            'ast': 0,
            'stl': 0,
            'blk': 0,
            'tov': 0,
            'foul': 0,
            'pts': 0
            }
    raw_opp_stats = {
            'fg': 0,
            'fga': 0,
            '3p': 0,
            '3pa': 0,
            '2p': 0,
            '2pa': 0,
            'ft': 0,
            'fta': 0,
            'drb': 0,
            'orb': 0,
            'ast': 0,
            'stl': 0,
            'blk': 0,
            'tov': 0,
            'foul': 0,
            'pts': 0
            }
    time_played = 0
    games_played = 0

    for f in gamefiles:
        in_game = False
        gamelog = open(f, 'r')
        lines = gamelog.readlines()
        gamelog.close()
        
        if team == f[-7:-4]: # indicates that team is the home team
            player_index = 8
        elif team == f[-11:-8]:
            player_index = 3
        else:
            continue

        for i in range(1, len(lines)):
            line = lines[i].split(',')
            
            # determine if the given lineup is involved
            players_in = 0
            if not whole_team:
                for j in range(5):
                    if line[player_index + j] in players:
                        players_in += 1
            if players_in == 5 or players_in == len(players) or whole_team:
                # the current lineup is playing, so let's do stuff
                time_played += convert_time(line[18])
                if not in_game:
                    in_game = True
                    games_played += 1

                # made shots
                if line[21] == 'shot':
                    if line[20] == team:
                        raw_stats['fg'] += 1
                        raw_stats['fga'] += 1
                    else:
                        raw_opp_stats['fg'] += 1
                        raw_opp_stats['fga'] += 1

                # made 3pt
                if line[21] == 'shot' and line[32] == '3':
                    if line[20] == team:
                        raw_stats['3p'] += 1
                        raw_stats['3pa'] += 1
                    else:
                        raw_opp_stats['3p'] += 1
                        raw_opp_stats['3pa'] += 1
                
                # made 2pt
                if line[21] == 'shot' and line[32] == '2':
                    if line[20] == team:
                        raw_stats['2p'] += 1
                    else:
                        raw_opp_stats['2p'] += 1
                
                # made ft
                if line[21] == 'free throw' and line[32] == '1':
                    if line[20] == team:
                        raw_stats['ft'] += 1
                        raw_stats['fta'] += 1
                    else:
                        raw_opp_stats['ft'] += 1
                        raw_opp_stats['fta'] += 1

                # missed shots are still attempts
                if line[21] == 'miss':
                    if line[20] == team:
                        raw_stats['fga'] += 1
                    else:
                        raw_opp_stats['fga'] += 1

                # missed 3pt
                if line[21] == 'miss' and '3PT' in line[43]:
                    if line[20] == team:
                        raw_stats['3pa'] += 1
                    else:
                        raw_opp_stats['3pa'] += 1

                # missed 2pt
                if line[21] == 'miss' and '3PT' not in line[43]:
                    if line[20] == team:
                        raw_stats['2pa'] += 1
                    else:
                        raw_opp_stats['2pa'] += 1

                # missed ft
                if line[21] == 'free throw' and line[32] == '0':
                    if line[20] == team:
                        raw_stats['fta'] += 1
                    else:
                        raw_opp_stats['fta'] += 1

                # drb
                if line[37] == 'rebound defensive':
                    if line[20] == team:
                        raw_stats['drb'] += 1
                    else:
                        raw_opp_stats['drb'] += 1

                # orb
                if line[37] == 'rebound offensive':
                    if line[20] == team:
                        raw_stats['orb'] += 1
                    else:
                        raw_opp_stats['orb'] += 1

                # ast
                if line[22]:
                    if line[20] == team:
                        raw_stats['ast'] += 1
                    else:
                        raw_opp_stats['ast'] += 1

                # stl
                if 'STEAL' in line[43]:
                    if line[20] != team:
                        raw_stats['stl'] += 1
                    else:
                        raw_opp_stats['stl'] += 1

                # blk
                if line[25]:
                    if line[20] != team:
                        raw_stats['blk'] += 1
                    else:
                        raw_opp_stats['blk'] += 1

                # tov
                if line[21] == 'turnover':
                    if line[20] == team:
                        raw_stats['tov'] += 1
                    else:
                        raw_opp_stats['tov'] += 1

                # foul
                if line[21] == 'foul':
                    if line[20] == team:
                        raw_stats['foul'] += 1
                    else:
                        raw_opp_stats['foul'] += 1

                # pts
                if line[32]:
                    if line[20] == team:
                        raw_stats['pts'] += int(line[32])
                    else:
                        raw_opp_stats['pts'] += int(line[32])

    # estimate possessions with formula
    try:
        poss = 0.5 * ((raw_stats['fga'] + 0.4 * raw_stats['fta'] - 1.07 * \
                (raw_stats['orb'] / (raw_stats['drb'] + raw_stats['orb'])) * \
                (raw_stats['fga'] - raw_stats['fg']) + raw_stats['tov']) + \
                (raw_stats['fga'] + 0.4 * raw_stats['fta'] - 1.07 * \
                (raw_stats['orb'] / (raw_stats['drb'] + raw_stats['orb'])) * \
                (raw_stats['fga'] - raw_stats['fg']) + raw_stats['tov']))
    except:
        poss = 0
    if poss == 0:
        per_poss = 0
    else:
        per_poss = 100 / poss

    stats = {
            'poss': 0,
            'min': 0,
            'fg': 0,
            'fga': 0,
            'fg%': 0,
            '3p': 0,
            '3pa': 0,
            '3p%': 0,
            '2p': 0,
            '2pa': 0,
            '2p%': 0,
            'ft': 0,
            'fta': 0,
            'ft%': 0,
            'orb': 0,
            'drb': 0,
            'ast': 0,
            'stl': 0,
            'blk': 0,
            'tov': 0,
            'pf': 0,
            'ortg': 0,
            'drtg': 0,
            'ts%': 0,
            'efg%': 0,
            'to%': 0,
            'orb%': 0,
            'ftr': 0,
            'pts': 0,
            }
    opp_stats = {
            'poss': 0,
            'min': 0,
            'fg': 0,
            'fga': 0,
            'fg%': 0,
            '3p': 0,
            '3pa': 0,
            '3p%': 0,
            '2p': 0,
            '2pa': 0,
            '2p%': 0,
            'ft': 0,
            'fta': 0,
            'ft%': 0,
            'orb': 0,
            'drb': 0,
            'ast': 0,
            'stl': 0,
            'blk': 0,
            'tov': 0,
            'pf': 0,
            'ortg': 0,
            'drtg': 0,
            'ts%': 0,
            'efg%': 0,
            'to%': 0,
            'orb%': 0,
            'ftr': 0,
            'pts': 0,
            }

    stats['poss'] = poss
    stats['min'] = time_played
    stats['fg'] = raw_stats['fg'] * per_poss
    stats['fga'] = raw_stats['fga'] * per_poss
    if raw_stats['fga'] == 0:
        stats['fg%'] = 0
    else:
        stats['fg%'] = raw_stats['fg'] / raw_stats['fga']
    stats['3p'] = raw_stats['3p'] * per_poss
    stats['3pa'] = raw_stats['3pa'] * per_poss
    if raw_stats['3pa'] == 0:
        stats['3p%'] = 0
    else:
        stats['3p%'] = raw_stats['3p'] / raw_stats['3pa']
    stats['2p'] = raw_stats['2p'] * per_poss
    stats['2pa'] = raw_stats['2pa'] * per_poss
    if raw_stats['2pa'] == 0:
        stats['2p%'] = 0
    else:
        stats['2p%'] = raw_stats['2p'] / raw_stats['2pa']
    stats['ft'] = raw_stats['ft'] * per_poss
    stats['fta'] = raw_stats['ft'] * per_poss
    if raw_stats['fta'] == 0:
        stats['ft%'] = 0
    else:
        stats['ft%'] = raw_stats['ft'] / raw_stats['fta']
    stats['drb'] = raw_stats['drb'] * per_poss
    stats['orb'] = raw_stats['orb'] * per_poss
    stats['ast'] = raw_stats['ast'] * per_poss
    stats['stl'] = raw_stats['stl'] * per_poss
    stats['blk'] = raw_stats['blk'] * per_poss
    stats['tov'] = raw_stats['tov'] * per_poss
    stats['foul'] = raw_stats['foul'] * per_poss
    stats['ortg'] = raw_stats['pts'] * per_poss
    stats['drtg'] = raw_opp_stats['pts'] * per_poss
    if raw_stats['fga'] + raw_stats['fta'] == 0:
        stats['ts%'] = 0
    else: 
        stats['ts%'] = raw_stats['pts'] / \
          (2 * (raw_stats['fga'] + 0.44 * raw_stats['fta']))
    if raw_stats['fga'] == 0:
        stats['efg%'] = 0
    else:
        stats['efg%'] = (0.5 * raw_stats['3p'] + raw_stats['fg']) \
                / raw_stats['fga']
    if poss == 0:
        stats['to%'] = 0
    else:
        stats['to%'] = raw_stats['tov'] / poss
    if raw_stats['orb'] + raw_opp_stats['drb'] == 0:
        stats['orb%'] = 0
    else:
        stats['orb%'] = raw_stats['orb'] / (raw_stats['orb'] + \
                raw_opp_stats['drb'])
    if raw_stats['fga'] == 0:
        stats['ftr'] = 0
    else:
        stats['ftr'] = raw_stats['fta'] / raw_stats['fga']
    stats['pts'] = raw_stats['pts']

    opp_stats['poss'] = poss
    opp_stats['min'] = time_played
    opp_stats['fg'] = raw_opp_stats['fg'] * per_poss
    opp_stats['fga'] = raw_opp_stats['fga'] * per_poss
    if raw_opp_stats['fga'] == 0:
        opp_stats['fg%'] = 0
    else:
        opp_stats['fg%'] = raw_opp_stats['fg'] / raw_opp_stats['fga']
    opp_stats['3p'] = raw_opp_stats['3p'] * per_poss
    opp_stats['3pa'] = raw_opp_stats['3pa'] * per_poss
    if raw_opp_stats['3pa'] == 0:
        opp_stats['3p%'] = 0
    else:
        opp_stats['3p%'] = raw_opp_stats['3p'] / raw_opp_stats['3pa']
    opp_stats['2p'] = raw_opp_stats['2p'] * per_poss
    opp_stats['2pa'] = raw_opp_stats['2pa'] * per_poss
    if raw_opp_stats['2pa'] == 0:
        opp_stats['2p%'] = 0
    else:
        opp_stats['2p%'] = raw_opp_stats['2p'] / raw_opp_stats['2pa']
    opp_stats['ft'] = raw_opp_stats['ft'] * per_poss
    opp_stats['fta'] = raw_opp_stats['fta'] * per_poss
    if raw_opp_stats['fta'] == 0:
        opp_stats['ft%'] = 0
    else:
        opp_stats['ft%'] = raw_opp_stats['ft'] / raw_opp_stats['fta']
    opp_stats['drb'] = raw_opp_stats['drb'] * per_poss
    opp_stats['orb'] = raw_opp_stats['orb'] * per_poss
    opp_stats['ast'] = raw_opp_stats['ast'] * per_poss
    opp_stats['stl'] = raw_opp_stats['stl'] * per_poss
    opp_stats['blk'] = raw_opp_stats['blk'] * per_poss
    opp_stats['tov'] = raw_opp_stats['tov'] * per_poss
    opp_stats['foul'] = raw_opp_stats['foul'] * per_poss
    opp_stats['ortg'] = raw_opp_stats['pts'] * per_poss
    opp_stats['drtg'] = raw_stats['pts'] * per_poss
    if raw_opp_stats['fga'] + raw_opp_stats['fta'] == 0:
        opp_stats['ts%'] = 0
    else:
        opp_stats['ts%'] = raw_opp_stats['pts'] / \
          (2 * (raw_opp_stats['fga'] + 0.44 * raw_opp_stats['fta']))
    if raw_stats['fga'] == 0:
        stats['efg%'] = 0
    else:
        stats['efg%'] = (0.5 * raw_stats['3p'] + raw_stats['fg']) / \
                raw_stats['fga']
    if poss == 0:
        stats['to%'] = 0
    else:
        stats['to%'] = raw_stats['tov'] / poss
    if raw_stats['orb'] + raw_opp_stats['drb'] == 0:
        stats['orb%'] = 0
    else:
        stats['orb%'] = raw_stats['orb'] / (raw_stats['orb'] + \
                raw_opp_stats['drb'])
    if raw_stats['fga'] == 0:
        stats['ftr'] = 0
    else:
        stats['ftr'] = raw_stats['fta'] / raw_stats['fga']
    opp_stats['pts'] = raw_opp_stats['pts']

    if return_raw:
        return stats, opp_stats, raw_stats, raw_opp_stats, games_played
    else:
        return stats, opp_stats, games_played

def get_players(gamefile):
    """
    Returns the home and away players that played in a game.
    """
    f = open(gamefile, "r")
    lines = f.readlines()
    f.close()

    home_roster = []
    away_roster = []

    for line in lines:
        for i in range(5):
            if line[8 + i] not in home_roster:
                home_roster.append(line[8 + i])
            if line[3 + i] not in away_roster:
                away_roster.append(line[3 + i])

    return home_roster, away_roster

def get_lineups(gamefile):
    """
    returns all lineups used in the game, but not other stats
    """
    f = open(gamefile, "r")
    lines = f.readlines()
    f.close()

    home_lineups = []
    away_lineups = []

    for line in lines:
        home_lineup = []
        away_lineup = []
        for i in range(5):
            away_lineup.append(line[3 + i])
            home_lineup.append(line[8 + i])
            if away_lineup not in away_lineups:
                away_lineups.append(away_lineup)
            if home_lineup not in home_lineups:
                home_lineups.append(home_lineup)

    return home_lineups, away_lineups
