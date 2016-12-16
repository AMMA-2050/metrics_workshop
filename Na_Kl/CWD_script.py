import os
import matplotlib.pyplot as plt
import numpy as np
import iris
import iris.quickplot as qplt

def count_wet():

    data = iris.load_cube('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/MIROC5/historical/pr_WFDEI_1979-2013_0.5x0.5_day_MIROC5_africa_historical_r1i1p1_full.nc')
    precip=data.intersection(latitude=(2.0, 12.0), longitude=(-20.0, 20.0))
    #iris.coord_categorisation.add_season(precip, 'time',name='season', seasons='jja')   
    precip.convert_units('kg m-2 day-1')
     #print(axis)    
    # Threshold the data to find the 'significant' points.
    # Make an array with data values "windowed" along the time axis.
    #hit_windows = iris.util.rolling_window(data_hits, window=wet_length, axis=axis) # rolling window along time axis
    #full_windows = np.all(hit_windows, axis=axis+1)
    #wet_point_counts = np.sum(full_windows, axis=axis, dtype=int)
    #return wet_point_counts
    
    count = iris.analysis.Aggregator('wet_count',count_wet,
                                 units_func=lambda units: 1)
                                 
    # Define the parameters of the aggregation:
    thresh_rain = 1
    wet_days = 10

    # Calculate the statistic.
    wet = precip.collapsed('time', count,threshold=thresh_rain,
                                      wet_length=wet_days)
    wet.rename('Number of days with rain > 1mm day-1 over 10 consecutive days')   

    qplt.contourf(wet)
    d = plt.gca() # get axis object
    d.coastlines() # to draw coastlines 
    plt.show()
       
if __name__ == "__main__":
    count_wet()  
        
        
        