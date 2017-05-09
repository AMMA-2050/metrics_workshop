# -*- coding: utf-8 -*-
"""

Created on Tue Jan 31 12:00:35 2017
Number of days Tmax > threshold (for period). Set threshold at 34 degrees C for now?

@author: siny
"""

import os
import iris
import iris.coord_categorisation 

def variable_setter(string):

        if string == 'var':
           string = 'Tas'
        if string == 'plot_type':
           string = 'contourf_map'
        if string == 'seas':
           string = 'jjas'
        return(string)



if "__name__" == "__variable_setter__":
        variable_setter(string)


def getSeasConstr(name):

    sncon = {'ann': iris.Constraint(month_number=lambda cell: 1 <= cell <= 12),
            'mj' : iris.Constraint(month_number=lambda cell: 5 <= cell <= 6),
            'jj' : iris.Constraint(month_number=lambda cell: 6 <= cell <= 7),
            'ja' : iris.Constraint(month_number=lambda cell: 7 <= cell <= 8),
            'as' : iris.Constraint(month_number=lambda cell: 8 <= cell <= 9),
            'so' : iris.Constraint(month_number=lambda cell: 9 <= cell <= 10),
            'jan' :  iris.Constraint(month_number=lambda cell: cell == 1),
            'feb' :  iris.Constraint(month_number=lambda cell: cell == 2),
            'mar' :  iris.Constraint(month_number=lambda cell: cell == 3),
            'apr' :  iris.Constraint(month_number=lambda cell: cell == 4),
            'may' :  iris.Constraint(month_number=lambda cell: cell == 5),
            'jun' :  iris.Constraint(month_number=lambda cell: cell == 6),
            'jul' :  iris.Constraint(month_number=lambda cell: cell == 7),
            'aug' :  iris.Constraint(month_number=lambda cell: cell == 8),
            'sep' :  iris.Constraint(month_number=lambda cell: cell == 9),
            'oct' :  iris.Constraint(month_number=lambda cell: cell == 10),
            'nov' :  iris.Constraint(month_number=lambda cell: cell == 11),
            'dec' :  iris.Constraint(month_number=lambda cell: cell == 12),
            'djf': iris.Constraint(month_number=lambda cell: (cell == 12) | (1 <= cell <= 2)),
            'mam': iris.Constraint(month_number=lambda cell: 3 <= cell <= 5),
            'jja': iris.Constraint(month_number=lambda cell: 6 <= cell <= 8),
            'jas': iris.Constraint(month_number=lambda cell: 7 <= cell <= 9),
            'jjas': iris.Constraint(month_number=lambda cell: 6 <= cell <= 9),
            'mjjas': iris.Constraint(month_number=lambda cell: 5<= cell<=9),
            'son': iris.Constraint(month_number=lambda cell: 9 <= cell <= 11)
            }

    return(sncon[name])




if __name__ == "__getSeasConstr__":
   getSeasConstr(season)




def main(cubein,season,ncfile):
	'''
	This file calculates the number of days Tmax > 34C
	'''


    iris.coord_categorisation.add_month_number(cubein,'time',name = 'month_number')
    iris.coord_categorisation.add_year(cubein,'time',name='year')
    iris.coord_categorisation.add_day_of_year(cubein,'time',name='day_of_year')
    slicer = getSeasConstr(season)
    cubein = cubein.extract(slicer)
    cubein.convert_units('Celsius') # convert unit
    Ts=34
    Numday = cubein.aggregated_by('time', iris.analysis.COUNT, function = lambda values: values > Ts )
    iris.save(Numday,ncfile)
    print(Numday)

    # Here i test this method using a times series variables
#    Tmax=cube
#    Tmax.coord('latitude').guess_bounds()
#    Tmax.coord('longitude').guess_bounds()
#    Tseries=Tmax.collapsed(['longitude', 'latitude'], iris.analysis.MEAN)
#    Tse=34
#    Numday = Tseries.aggregated_by('time', iris.analysis.COUNT, function = lambda values: values > Tse )

if __name__ == "__main__":
	main(cubein,season,ncfile)

