"""
Here we examine using the four factors to predict point
differential in games.
"""

from sklearn import linear_model
import gamestats as gs
import numpy as np
import misc

make_model(dates):
    """
    makes the linear regression model for the four factors between
    the given dates.
    """
    team_combos = []
    for i in range(30):
        for j in range(30):
            if i != j:
                team_combos.append([misc.ALL_TEAMS[i], misc.ALL_TEAMS[j])

    gamefiles = gs.find_gamefiles(dates, team_combos)

    x = np.zeros((len(gamefiles), 8))
    y = no.zeros(len(gamefiles))

    row = 0
    for gamefile in gamefiles:
        hometeam = gamefiles[-7:-4]
        stats, opp_stats, raw_stats, raw_opp_stats, _ = \
                gs.get_lineup_stats(hometeam, [gamefile], \
                return_raw = True, whole_team = True)
        x[row][0] = stats['efg']
        x[row][1] = stats['ftr']
        x[row][2] = stats['tov']
        x[row][3] = stats['orb']
        x[row][4] = opp_stats['efg']
        x[row][5] = opp_stats['ftr']
        x[row][6] = opp_stats['tov']
        x[row][7] = opp_stats['orb']
        y[row] = raw_stats['pts'] - raw_opp_stats['pts']
        row += 1


    return -1
