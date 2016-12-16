'''
This is Bamba's code to compute the standardized Precipitation Index at 3 month period (SPI)
during the metrics_workshop. Go thoughout en Enjoy it!
'''
import os
import iris
import iris.coord_categorisation 
from iris.experimental.equalise_cubes import equalise_attributes
import iris.quickplot as qplt
import matplotlib.pyplot as plt
import numpy as np

def calcSPI(incube, period_mon, outfile):
    try:
        spi = iris.load_cube(outfile) 

    except IOError:
       	   
        incube.coord('latitude').guess_bounds()
        incube.coord('longitude').guess_bounds()
        iris.coord_categorisation.add_month_number(incube, 'time', name='month')
        iris.coord_categorisation.add_year(incube, 'time', name='year')
    
        c_monthly = incube.aggregated_by(['month','year'], iris.analysis.MEAN)
        #iris.save(c_monthly, 'mean.nc')
        
        c_monthly.convert_units('kg m-2 day-1')
        
        # This is the monthly climatology (mean and std deviation) 
        # Shape of these files: (12, 54, 80)
        std = c_monthly.aggregated_by('month', iris.analysis.STD_DEV)
        mean = c_monthly.aggregated_by('month', iris.analysis.MEAN)
        
        # We need to change the shape of the monthly climatologies to match the shape of the timeseries (in the cube c_monthly)
        # Shape of c_monthly: (672, 54, 80)
        clim_mean_data = np.tile(mean.data, (c_monthly.shape[0]/mean.shape[0],1,1))
        clim_std_data = np.tile(std.data, (c_monthly.shape[0]/std.shape[0],1,1))
        
        clim_mean_cube = c_monthly.copy(clim_mean_data)
        clim_std_cube = c_monthly.copy(clim_std_data)
        
        spi = (c_monthly - clim_mean_cube) / clim_std_cube              

    return(spi)
