"""
miscellaneous helper functions
"""

def convert_to_date(datestring):
    """
    returns date from a string with format
    datestring = 'yyyy-mm-dd'
    """
    year = int(datestring[:4])
    month = int(datestring[5:7])
    day = int(datestring[8:10])
    return date(year,month,day)


