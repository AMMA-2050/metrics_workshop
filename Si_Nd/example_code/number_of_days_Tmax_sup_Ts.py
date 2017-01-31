# -*- coding: utf-8 -*-
"""

Created on Tue Jan 31 12:00:35 2017
Number of days Tmax > threshold (for period). Set threshold at 34 degrees C for now?

@author: siny
"""

import os
import iris
import iris.coord_categorisation 




def number_of_days_Tmax_sup_Ts(cube):
    print "Here we calculate the number of day Tmax > Ts"
       
    iris.coord_categorisation.add_month_number(cube, 'time', name='month')
    cube.convert_units('Celsius') # convert unit
    Ts=34
    Numday = cube.aggregated_by('time', iris.analysis.COUNT, function = lambda values: values > Ts )
    print(Numday)
    # Here i test this method using a times series variables
    Tmax=cube
    Tmax.coord('latitude').guess_bounds()
    Tmax.coord('longitude').guess_bounds()
    Tseries=Tmax.collapsed(['longitude', 'latitude'], iris.analysis.MEAN)
    Tse=34
    Numday = Tseries.aggregated_by('time', iris.analysis.COUNT, function = lambda values: values > Tse )



