'''
This is the master script that controls the processing chain
'''
import iris
import numpy as np
# Import local scripts

def loadDaily(inpath, modname, regname, dtyp):
    '''
    Returns an iris cube for the daily data, clipped to the region of interest
    Inputs
        - inpath  : the path to the folder that contains the different data types (chr string)
        - modname : the model to retrieve the data for (chr string)
        - regname : the region that we want the data for (chr string)
        - dtyp    : the folder name that describes whether the data was downscaled, bias corrected etc
    Outputs
        - ocube   : a cube of the daily data that matches the specifications
    
    Author: Andy Hartley, 12/12/2016
    '''
    
    
def loadMonthly(inpath, modname, stat, regname, dtyp)
    '''
    Returns an iris cube for the monthly aggregated data, clipped to the region of interest
    Inputs
        - inpath  : the path to the folder that contains the different data types (chr string)
        - modname : the model to retrieve the data for (chr string)
        - stat    : the name of the statistic to be calculated (chr string) e.g. mean, min, max, etc
        - regname : the region that we want the data for (chr string)
        - dtyp    : the folder name that describes whether the data was downscaled, bias corrected etc
    Outputs
        - ocube   : a cube of the daily data that matches the specifications
    Author: Andy Hartley, 12/12/2016
    '''

def constrainByTime(incube, start_yr, end_yr, aggperiod):
    '''
    Returns a cube of daily time-series constrained by a climate period and either a month or season
    Inputs
        - incube     : a daily timeseries for the full 1950 to 2100 period
        - start_yr   : the start of a multi-year period to extract from the data. Output includes the given year (int)
        - end_yr     : the end of a multi-year period to extract from the data. Output includes the given year (int)
        - aggperiod  : a month or season for which to aggregate
    Outputs
        - ocube      : a daily time-series that contains only the periods specified
    Author: Andy Hartley, 12/12/2016
    '''
    sncon = {'ann': iris.Constraint(month_number=lambda cell: 1 <= cell <= 12),
              'mj' : iris.Constraint(month_number=lambda cell: 5 <= cell <= 6),
              'jj' : iris.Constraint(month_number=lambda cell: 6 <= cell <= 7),
              'ja' : iris.Constraint(month_number=lambda cell: 7 <= cell <= 8),
              'as' : iris.Constraint(month_number=lambda cell: 8 <= cell <= 9),
              'so' : iris.Constraint(month_number=lambda cell: 9 <= cell <= 10),
              'jan' :  iris.Constraint(month_number=lambda cell: cell == 1),
              'feb' :  iris.Constraint(month_number=lambda cell: cell == 2),
              'mar' :  iris.Constraint(month_number=lambda cell: cell == 3),
              'apr' :  iris.Constraint(month_number=lambda cell: cell == 4),
              'may' :  iris.Constraint(month_number=lambda cell: cell == 5),
              'jun' :  iris.Constraint(month_number=lambda cell: cell == 6),
              'jul' :  iris.Constraint(month_number=lambda cell: cell == 7),
              'aug' :  iris.Constraint(month_number=lambda cell: cell == 8),
              'sep' :  iris.Constraint(month_number=lambda cell: cell == 9),
              'oct' :  iris.Constraint(month_number=lambda cell: cell == 10),
              'nov' :  iris.Constraint(month_number=lambda cell: cell == 11),
              'dec' :  iris.Constraint(month_number=lambda cell: cell == 12),
              'djf': iris.Constraint(month_number=lambda cell: (cell == 12) | (1 <= cell <= 2)),
              'mam': iris.Constraint(month_number=lambda cell: 3 <= cell <= 5),
              'jja': iris.Constraint(month_number=lambda cell: 6 <= cell <= 8),
              'jas': iris.Constraint(month_number=lambda cell: 7 <= cell <= 9),
              'son': iris.Constraint(month_number=lambda cell: 9 <= cell <= 11)
              }
    
    # Check that the incube has month_number and season_year coordinates, if not create them ...
    if incube.coord('month_number')
    
    # Create a year constraint ...
    yrcon = iris.Constraint(season_year = lambda cell, minyr=start_yr, maxyr=end_yr: minyr <= cell <= maxyr)
    incube_clim = model_cube.extract(yrcon)
    
    # Create a season constraint ...
    ocube = incube_clim.extract(sncon[seas])
    
    return(ocube)
    