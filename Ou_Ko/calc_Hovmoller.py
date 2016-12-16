'''
calc_Hovmoller.py
'''


import iris
import numpy as np
import scipy as sci
import iris.coord_categorisation


def calc_Hovmoller(cubein,season,ncfile):
    
       print ' This is cal_script'
       reg_cube_coll = cubein.collapsed('longitude', iris.analysis.MEAN)
       iris.coord_categorisation.add_month_number(reg_cube_coll, 'time', name='month')
       cube2plot =  reg_cube_coll.aggregated_by('month',iris.analysis.MEAN)      
       cube2plot.convert_units('kg m-2 day-1')
       print cube2plot
#       iris.save(cube2plot, str(ncfile))


if __name__ == "__main__": 
    calc_Hovmoller(cubein,season,ncfile) 