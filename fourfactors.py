"""
Here we examine using the four factors to predict point
differential in games.
"""

import gamestats as gs
import numpy as np
import sklean as sk
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

    gamefiles = gs.find_gamefiles(dates)

    return -1
