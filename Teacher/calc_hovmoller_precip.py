'''
calc_hovmoller_precip.py
'''



import iris
import numpy as np
import scipy as sci
import matplotlib.pyplot as plt
import iris.coord_categorisation


def calc_hovmoller_precip(cubein,season,ncfile):

	print 'This is the calc script'
        reg_cube_coll = cubein.collapsed('longitude', iris.analysis.MEAN)    
        iris.coord_categorisation.add_month_number(reg_cube_coll, 'time', name='month')
        cube2plot = reg_cube_coll.aggregated_by('month', iris.analysis.MEAN)
        cube2plot.convert_units('kg m-2 day-1')     
#        iris.save(cube2plot,str(ncfile))
        iris.save(cube2plot,ncfile)
        
        return cube2plot







if __name__ == "__main__":
	calc_hovmoller_precip(cubein,season,ncfile)
