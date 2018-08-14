"""
Here we examine using the four factors to predict point
differential in games.
"""

from sklearn import linear_model as lm
from sklearn.metrics import r2_score
import gamestats as gs
import numpy as np
import matplotlib.pyplot as plt
import misc
from datetime import timedelta

def make_model(dates):
    """
    makes the linear regression model for the four factors between
    the given dates.
    """
    team_combos = []
    for i in range(30):
        for j in range(30):
            if i != j:
                team_combos.append([misc.ALL_TEAMS[i], misc.ALL_TEAMS[j]])

    gamefiles = gs.find_gamefiles(dates, team_combos)

    x = np.zeros((len(gamefiles), 8))
    y = np.zeros(len(gamefiles))

    row = 0
    for gamefile in gamefiles:
        hometeam = gamefile[-7:-4]
        print(gamefile)
        stats, opp_stats, raw_stats, raw_opp_stats, _ = \
                gs.get_lineup_stats(hometeam, [], [gamefile], \
                return_raw = True, whole_team = True)
        x[row][0] = stats['efg%']
        x[row][1] = stats['ftr']
        x[row][2] = stats['to%']
        x[row][3] = stats['orb%']
        x[row][4] = opp_stats['efg%']
        x[row][5] = opp_stats['ftr']
        x[row][6] = opp_stats['to%']
        x[row][7] = opp_stats['orb%']
        y[row] = raw_stats['pts'] - raw_opp_stats['pts']
        row += 1

    linear = lm.LinearRegression(normalize = True)
    linear.fit(x, y)

    y_pred = linear.predict(x)

    print(linear.coef_)
    print(linear.intercept_)
    print(r2_score(y, y_pred))

    return -1

def visualize_factors(team, dates):
    """
    Plots 8 graphs for how the teams overall four factors
    change during the given time frame.

    team = three letter team code string, e.g., "CLE"
    dates as usual.
    """
    team_combos = []
    for i in range(len(misc.ALL_TEAMS)):
        team_combos.append([team, misc.ALL_TEAMS[i]])
        team_combos.append([misc.ALL_TEAMS[i], team])

    startdate = misc.convert_to_date(dates[0])
    enddate = misc.convert_to_date(dates[1])
    diffdays = (enddate - startdate).days

    categories = ['efg%', 'to%', 'orb%', 'ftr', 'opp_efg%', \
            'opp_to%','opp_orb%', 'opp_ftr']
    d_stats = dict([(x, []) for x in categories])
    d_diffs = dict([(x, []) for x in categories])

    for i in range(diffdays):
        # get the stats for the date range, append data to proper lists
        # construct the date range strings as [dates[0], str(dates[0]+i days)]
        today = (startdate + timedelta(days = i)).strftime('%Y-%m-%d')
        gamefiles = gs.find_gamefiles([dates[0], today], team_combos)

        if len(gamefiles) > len(d_stats[categories[0]]):
            # this is bad, going over same files over and over again
            stats, opp_stats, _ = \
                    gs.get_lineup_stats(team, [], gamefiles, \
                    return_raw = False, whole_team = True)
            for x in categories:
                if x[0:3] == 'opp':
                    d_stats[x].append(opp_stats[x[4:]])
                else:
                    d_stats[x].append(stats[x])

    # make the percentage change lists
    for i in range(len(d_stats['efg%']) - 1):
        for x in categories:
            d_diffs[x].append(100 * 
                    (d_stats[x][i + 1] - d_stats[x][i]) / abs(d_stats[x][i]))


    fig, axes = plt.subplots(3, 3)

    # plot the stats
    j = 0
    for i in [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]]:
        ax = axes[i[0], i[1]]
        color = 'tab:blue'
        ax.set_xlabel('game #')
        ax.set_ylabel(categories[j], color = color)
        ax.plot(range(1, len(d_stats[categories[j]]) + 1), \
                d_stats[categories[j]], color = color)
        ax.tick_params(axis = 'y', labelcolor = color)

        ax2 = ax.twinx()

        color = 'tab:red'
        ax2.set_ylabel('percent change', color = color)
        ax2.plot(range(2, len(d_stats[categories[j]]) + 1), \
                d_diffs[categories[j]], color = color)
        ax2.tick_params(axis = 'y', labelcolor = color)
        j += 1

    # plot the middle stuff
    axes[1, 1].axis([-1, 1, -1, 1])
    axes[1, 1].text(0, 0.1, team, fontsize = 14, weight = 'bold',
            ha = 'center', color = misc.TEAM_COLORS[team][0],
            bbox = {'facecolor':misc.TEAM_COLORS[team][1],
                'alpha':0.5, 'pad':10})
    axes[1, 1].text(0, -0.4, dates, fontsize = 10, ha = 'center')
    axes[1, 1].axis('off')

    fig.tight_layout()
    plt.show()
    
    return -1

