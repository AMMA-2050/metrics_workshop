"""
Contains global constants for the CMIP5 atlas
"""

SCENARIO = ['historical', 'rcp26', 'rcp45', 'rcp85']

AGGREGATION = ['tseries', '2d', 'trend']

FUT_TREND = [2010, 2060]
FUTURE = [2040, 2059]
HIST = [1950, 2000]

HOTDAYS_THRESHOLD = 40
RAINYDAY_THRESHOLD = 1
STRONGWIND_THRESHOLD = 30 # Values in 1 sample file have a historical max of 7 to 9, so this value is still far too high

