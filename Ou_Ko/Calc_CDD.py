'''
Calc_CCD.py
'''
import os
import matplotlib.pyplot as plt
import numpy as np
import iris
import iris.quickplot as qplt
import iris.coord_categorisation


def calcDryDays(incube, outfile):
    
    
    try:
        mdrydays=iris.load_cube(outfile)

    except IOError:
    
        print 'Calculating Number of Dry Days per season'
        
        print incube
        
        iris.coord_categorisation.add_year(incube, 'time',name='year')        
        iris.coord_categorisation.add_season_year(incube, 'time',name='season_year')     
        iris.coord_categorisation.add_month_number(incube, 'time',name='month_number')
        incube.convert_units('kg m-2 day-1')
                
        drydays = incube.aggregated_by(['year','month_number'], iris.analysis.COUNT, function = lambda values: values <= 1.0 )
        
        print drydays
        
        mdrydays = drydays.aggregated_by('season_year', iris.analysis.MEAN)
        
        iris.save(mdrydays,outfile)
    
    return(mdrydays)    
    
    
#if __name__ == "__main__": 
    #calcDryDays(incube, outfile) 