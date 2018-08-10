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

    efgp = []
    top = []
    orbp = []
    ftr = []
    opp_efgp = []
    opp_top = []
    opp_orbp = []
    opp_ftr = []

    for i in range(diffdays):
        # get the stats for the date range, append data to proper lists
        # construct the date range strings as [dates[0], str(dates[0]+i days)]
        today = (startdate + timedelta(days = i)).strftime('%Y-%m-%d')
        gamefiles = gs.find_gamefiles([dates[0], today], team_combos)

        if len(gamefiles) > len(efgp):
            # this is bad, going over same files over and over again
            stats, opp_stats, _ = \
                    gs.get_lineup_stats(team, [], gamefiles, \
                    return_raw = False, whole_team = True)
            efgp.append(stats['efg%'])
            top.append(stats['to%'])
            orbp.append(stats['orb%'])
            ftr.append(stats['ftr'])
            opp_efgp.append(opp_stats['efg%'])
            opp_top.append(opp_stats['to%'])
            opp_orbp.append(opp_stats['orb%'])
            opp_ftr.append(opp_stats['ftr'])

    # make the percentage change lists
    diffs_efgp = []
    diffs_top = []
    diffs_orbp = []
    diffs_ftr = []
    diffs_opp_efgp = []
    diffs_opp_top = []
    diffs_opp_orbp = []
    diffs_opp_ftr = []
    for i in range(len(efgp) - 1):
        diffs_efgp.append((efgp[i + 1] - efgp[i]) / abs(efgp[i]))
        diffs_top.append((top[i + 1] - top[i]) / abs(top[i]))
        diffs_orbp.append((orbp[i + 1] - orbp[i]) / abs(orbp[i]))
        diffs_ftr.append((ftr[i + 1] - ftr[i]) / abs(ftr[i]))
        diffs_opp_efgp.append(
                (opp_efgp[i + 1] - opp_efgp[i]) / abs(opp_efgp[i]))
        diffs_opp_top.append((opp_top[i + 1] - opp_top[i]) / abs(opp_top[i]))
        diffs_opp_orbp.append(
                (opp_orbp[i + 1] - opp_orbp[i]) / abs(opp_orbp[i]))
        diffs_opp_ftr.append((opp_ftr[i + 1] - opp_ftr[i]) / abs(opp_ftr[i]))



    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) \
            = plt.subplots(3, 3)

    # the plot of the efg%
    color = 'tab:blue'
    ax1.set_xlabel('game #')
    ax1.set_ylabel('efg%', color = color)
    ax1.plot(range(1, len(efgp) + 1), efgp, color = color)
    ax1.tick_params(axis = 'y', labelcolor = color)

    ax12 = ax1.twinx()

    color = 'tab:red'
    ax12.set_ylabel('percent change', color = color)
    ax12.plot(range(2, len(efgp) + 1), diffs_efgp, color = color)
    ax12.tick_params(axis = 'y', labelcolor = color)

    # the plot of the to%
    color = 'tab:blue'
    ax2.set_xlabel('game #')
    ax2.set_ylabel('to%', color = color)
    ax2.plot(range(1, len(top) + 1), top, color = color)
    ax2.tick_params(axis = 'y', labelcolor = color)

    ax22 = ax2.twinx()

    color = 'tab:red'
    ax22.set_ylabel('percent change', color = color)
    ax22.plot(range(2, len(top) + 1), diffs_top, color = color)
    ax22.tick_params(axis = 'y', labelcolor = color)

    # the plot of the orb%
    color = 'tab:blue'
    ax3.set_xlabel('game #')
    ax3.set_ylabel('orb%', color = color)
    ax3.plot(range(1, len(orbp) + 1), orbp, color = color)
    ax3.tick_params(axis = 'y', labelcolor = color)

    ax32 = ax3.twinx()

    color = 'tab:red'
    ax32.set_ylabel('percent change', color = color)
    ax32.plot(range(2, len(orbp) + 1), diffs_orbp, color = color)
    ax32.tick_params(axis = 'y', labelcolor = color)

    # the plot of the ftr
    color = 'tab:blue'
    ax4.set_xlabel('game #')
    ax4.set_ylabel('free throw rate', color = color)
    ax4.plot(range(1, len(ftr) + 1), ftr, color = color)
    ax4.tick_params(axis = 'y', labelcolor = color)

    ax42 = ax4.twinx()

    color = 'tab:red'
    ax42.set_ylabel('percent change', color = color)
    ax42.plot(range(2, len(ftr) + 1), diffs_ftr, color = color)
    ax42.tick_params(axis = 'y', labelcolor = color)

    # plot of opp_efgp
    color = 'tab:blue'
    ax6.set_xlabel('game #')
    ax6.set_ylabel('opp efg%', color = color)
    ax6.plot(range(1, len(opp_efgp) + 1), opp_efgp, color = color)
    ax6.tick_params(axis = 'y', labelcolor = color)

    ax62 = ax6.twinx()

    color = 'tab:red'
    ax62.set_ylabel('percent change', color = color)
    ax62.plot(range(2, len(opp_efgp) + 1), diffs_opp_efgp, color = color)
    ax62.tick_params(axis = 'y', labelcolor = color)
    
    # plot of opp_top
    color = 'tab:blue'
    ax7.set_xlabel('game #')
    ax7.set_ylabel('opp to%', color = color)
    ax7.plot(range(1, len(opp_top) + 1), opp_top, color = color)
    ax7.tick_params(axis = 'y', labelcolor = color)

    ax72 = ax7.twinx()

    color = 'tab:red'
    ax72.set_ylabel('percent change', color = color)
    ax72.plot(range(2, len(opp_top) + 1), diffs_opp_top, color = color)
    ax72.tick_params(axis = 'y', labelcolor = color)
    
    # plot of opp_orbp
    color = 'tab:blue'
    ax8.set_xlabel('game #')
    ax8.set_ylabel('opp orb%', color = color)
    ax8.plot(range(1, len(opp_orbp) + 1), opp_orbp, color = color)
    ax8.tick_params(axis = 'y', labelcolor = color)

    ax82 = ax8.twinx()

    color = 'tab:red'
    ax82.set_ylabel('percent change', color = color)
    ax82.plot(range(2, len(opp_orbp) + 1), diffs_opp_orbp, color = color)
    ax82.tick_params(axis = 'y', labelcolor = color)

    # plot of opp_ftr
    color = 'tab:blue'
    ax9.set_xlabel('game #')
    ax9.set_ylabel('opp free throw rate', color = color)
    ax9.plot(range(1, len(opp_ftr) + 1), opp_ftr, color = color)
    ax9.tick_params(axis = 'y', labelcolor = color)

    ax92 = ax9.twinx()

    color = 'tab:red'
    ax92.set_ylabel('percent change', color = color)
    ax92.plot(range(2, len(opp_ftr) + 1), diffs_opp_ftr, color = color)
    ax92.tick_params(axis = 'y', labelcolor = color)

    ax5.set_xlabel(team)

    fig.tight_layout()
    plt.show()
    
    return -1

