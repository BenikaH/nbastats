"""
miscellaneous helper functions
"""

from datetime import date

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


