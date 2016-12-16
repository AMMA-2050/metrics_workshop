import matplotlib.pyplot as plt
import numpy as np

import iris
from iris.analysis import Aggregator
import iris.plot as iplt
import iris.quickplot as qplt
from iris.util import rolling_window


def count_spells(data, threshold, axis, spell_length):
    
    if axis < 0:
        
        axis += data.ndim
    
    data_hits = data > threshold
    
    hit_windows = rolling_window(data_hits, window=spell_length, axis=axis)
    
    full_windows = np.all(hit_windows, axis=axis+1)
    
    spell_point_counts = np.sum(full_windows, axis=axis, dtype=int)
    
    return spell_point_counts


def main():
    
    file_path = iris.sample_data_path('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/IPSL-CM5A-LR/historical/pr_WFDEI_1979-2013_0.5x0.5_day_IPSL-CM5A-LR_africa_historical_r1i1p1_full.nc')
    
    cube = iris.load_cube(file_path)
    
    cube_wafr = cube.intersection(latitude=(-10.0, 10.0), longitude=(4.0, 25.0))
    
    iris.coord_categorisation.add_year(cube_wafr, 'time',name='year')    
       
    iris.coord_categorisation.add_month_number(cube_wafr, 'time',name='month_number')
    
    iris.coord_categorisation.add_season(cube_wafr, 'time',name='season')
   
    SPELL_COUNT = Aggregator('spell_count', count_spells, units_func=lambda units: 1)

    threshold_rainfall = 0.1
    
    spell_days = 10

    dry_periods = cube.collapsed('time', SPELL_COUNT, threshold=threshold_rainfall, spell_length=spell_days)
    
    dry_periods.rename('Number of 10-days dry spells in 35 years')

    qplt.contourf(dry_periods, cmap='RdYlBu_r')
    
    plt.gca().coastlines()
    
    iplt.show()


if __name__ == '__main__':
    main()