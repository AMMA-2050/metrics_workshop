'''
calc_hovmoller_precip.py
'''
import numpy as np
import iris
import scipy as sci

def calc_hovmoller_precip(cubein,season,ncfile):
    
    """
    cubein should be a daily data
    Inputs
        -include: A 3D cube with time, lat and lon dimensions(iris cube)
        - figdir: An output path to write the figure to (chr string)
      Outputs  
        - a nice plot of the hovmuller!
    
    """
    iris.coord_categorisation.add_year(mycube_wafr, 'time',name='year')
    iris.coord_categorisation.add_season(mycube_wafr, 'time',name='season')
    iris.coord_categorisation.add_month_number(mycube_wafr, 'time',name='month_number')
    mycube_wafr.convert_units('kg m-2 day-1')
    
    
if __name__ == '__calc_hovmoller_precip__': 
    calc_hovmoller_precip(cubein, season, ncfile) 
        
        
