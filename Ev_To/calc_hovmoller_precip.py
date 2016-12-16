'''
calc_hovmoller_precip.py
'''
import iris
import numpy as np
import scipy as sci

def calc_hovmoller_precip(cubein,season,ncfile):
    
    print 'This is the calc script'
    reg_cube_coll = reg_cube.collapsed ('longitude', iriris.analysis.MEAN)
    iris.coord_categorisation.add_month_number(reg_cube_coll,'time', name='month')
    cube2plot = reg_cube_coll.agregated_by('month', iris.analysis.MEAN)
    cube2plot.convert_units('kg m-2 day-1')
    
    iris.save(cube2plot, str(ncfile))
    
if __name__=="__name__":
    calc_hovmoller_precip(cubein,season,ncfile)