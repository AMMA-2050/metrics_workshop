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
import pdb

def plot(infile, figpath):
     
    '''
    I am going to use data from HadGEM
    And I will be plotting nice fig of SPI
    '''  
    
def main():
    
    try:
        c_monthly = iris.load_cube('mean.nc') 
    except IOError:
       	   
        path = '/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/HadGEM2-ES/historical/pr_WFDEI_1979-2013_0.5x0.5_day_HadGEM2-ES_africa_historical_r1i1p1_full.nc'
        my_var = iris.load_cube(path)
    
        reg_cube = my_var.intersection(longitude=(-15.0, 25.0), latitude=(4.0, 31.0))
    
        reg_cube.coord('latitude').guess_bounds()
        reg_cube.coord('longitude').guess_bounds()
        #std = reg_cube.collapsed('longitude', iris.analysis.STD_DEV)
        #levels = np.arange(1,100)
        #mean = reg_cube.collapsed('longitude', iris.analysis.MEAN)
        iris.coord_categorisation.add_month_number(reg_cube, 'time', name='month')
        iris.coord_categorisation.add_year(reg_cube, 'time', name='year')
    
        c_monthly = reg_cube.aggregated_by(['month','year'], iris.analysis.MEAN)
        iris.save(c_monthly, 'mean.nc')
    
    c_monthly.convert_units('kg m-2 day-1')
    #iris.coord_categorisation.add_season(c_monthly, 'time', name='season', seasons=('djf', 'mam', 'jja', 'son'))
    #iris.coord_categorisation.add_season_year(c_monthly, 'time', name='season_year', seasons=('djf', 'mam', 'jja', 'son'))    
    
    
    #std = c_monthly.aggregated_by('season', iris.analysis.STD_DEV)
    #mean = c_monthly.aggregated_by('season', iris.analysis.MEAN)
    
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
    
    y_spi = (c_monthly - clim_mean_cube) / clim_std_cube
    
    spi_cotedivoire = y_spi.intersection(latitude=(4,12), longitude=(-2,9))
    spi_ts = spi_cotedivoire.collapsed(['latitude', 'longitude'], iris.analysis.MEAN)
    qplt.plot(spi_ts)
    
    #mean_per_year = c_monthly.aggregated_by(['season', 'season_year'], iris.analysis.MEAN)
    
    #yrs = mean_per_year.coord('season_year').points
    #yrs = c_monthly.coord('year').points
    #result = iris.cube.CubeList([])
    
    #spans_three_months = lambda t: (t.bound[1] - t.bound[0]) > 3*28
    #three_months_bound = iris.Constraint(time=spans_three_months)
    #full_season_means = mean_per_year.extract(three_months_bound)
#
#    u = np.unique(yrs)
#    print u
#    
#    for y in u:
#        print y
#        my_data_yr = c_monthly.extract(iris.Constraint(year=y))
#        print my_data_yr
#        container = my_data_yr.copy()
#        dat_yr = my_data_yr.data
#                       
#        dat_mean = mean.data
#        dat_std = std.data
#        
#        print y
#        print dat_yr.shape
#        print dat_mean.shape
#        print dat_std.shape
#                        
#        y_spi = (dat_yr - dat_mean) / dat_std
#   
#        container.data = y_spi
#        
#        result.append(container)
#       
#    print result.merge_cube()
#              
    #
    #pdb.set_trace()
    #plt.figure()            
    #qplt.pcolormesh(result[5][2,:,:])
    #plt.show()

       
if __name__== '__main__':
    main()