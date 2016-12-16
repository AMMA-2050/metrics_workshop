'''
calc_hovmuller_precip.py
'''

import iris
import numpy as np
import scipy as sci

def calc_hovmuller_precip(cubein,season,ncfile):
    print 'This is the calc script'
    reg_cull_coll = reg_cube.collapsed('longitude', iris.analysis.MEAN)      
    iris.coord_categorisation.add_month_number(reg_cull_coll, 'time', name='month')
    cube2plot = reg_cull_coll.aggregated_by('month', iris.analysis.MEAN)
    cube2plot.convert_units('kg m-2 day-1')
    iris.save(cube2plot, str(ncfile))

#if __name__ == "__main__":
#    calc_hovmuller_precip(cubein,season,ncfile)
