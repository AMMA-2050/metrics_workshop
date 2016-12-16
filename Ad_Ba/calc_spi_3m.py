'''
calc_spi_3m.py
'''
import os
import iris
import iris.coord_categorisation 
from iris.experimental.equalise_cubes import equalise_attributes
import iris.quickplot as qplt
import matplotlib.pyplot as plt
import numpy as np
import pdb
import scipy as sci

def calc_spi_3m(pr,season,ncfile):
    print 'this is the load data script'
    
    iris.coord_categorisation.add_season(c_monthly, 'time', name='season', seasons=('djf', 'mam', 'jja', 'son'))
    iris.coord_categorisation.add_season_year(c_monthly, 'time', name='season_year', seasons=('djf', 'mam', 'jja', 'son'))    
    
    
    std = c_monthly.aggregated_by('season', iris.analysis.STD_DEV)
    mean = c_monthly.aggregated_by('season', iris.analysis.MEAN)
    
    mean_per_year = c_monthly.aggregated_by(['season', 'season_year'], iris.analysis.MEAN)
    
    yrs = mean_per_year.coord('season_year').points
    result = iris.cube.CubeList([])
    container = mean_per_year.copy()
    
    u, ind = np.unique(yrs, return_index=True)
    
    for i, y in zip(ind, u):
        
        if y == 2006:      ### djf problem
            continue
            
        my_data_yr = mean_per_year.extract(iris.Constraint(season_year=y))
        dat_yr = my_data_yr.data
                       
        dat_mean = mean.data
        dat_std = std.data
                        
        y_spi = (dat_yr - dat_mean) / dat_std
        pdb.set_trace()    
        container[i:i+4].data = y_spi
        
        iris.save(y_spi,ncfile)
    
if __name__=="__main__":
    calc_spi_3m(pr,season,ncfile) 