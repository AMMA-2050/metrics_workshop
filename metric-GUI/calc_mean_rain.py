import iris
import numpy as np
import scipy as sci
import matplotlib.pyplot as plt
import iris.coord_categorisation
import pdb



def variable_setter(string):
	if string == 'var':
		string = 'pr'
	if string =='seas':
		string = 'jas'
	if string =='plot_type':
		string = 'plot_bar_year'
	return string

if "__name__" == "__variable_setter__":
    variable_setter(string)


def getSeasConstr(name):
    sncon = {'ann': iris.Constraint(month_number=lambda cell: 1 <= cell <= 12),
             'mj': iris.Constraint(month_number=lambda cell: 5 <= cell <= 6),
             'jj': iris.Constraint(month_number=lambda cell: 6 <= cell <= 7),
             'ja': iris.Constraint(month_number=lambda cell: 7 <= cell <= 8),
             'as': iris.Constraint(month_number=lambda cell: 8 <= cell <= 9),
             'so': iris.Constraint(month_number=lambda cell: 9 <= cell <= 10),
             'jan': iris.Constraint(month_number=lambda cell: cell == 1),
             'feb': iris.Constraint(month_number=lambda cell: cell == 2),
             'mar': iris.Constraint(month_number=lambda cell: cell == 3),
             'apr': iris.Constraint(month_number=lambda cell: cell == 4),
             'may': iris.Constraint(month_number=lambda cell: cell == 5),
             'jun': iris.Constraint(month_number=lambda cell: cell == 6),
             'jul': iris.Constraint(month_number=lambda cell: cell == 7),
             'aug': iris.Constraint(month_number=lambda cell: cell == 8),
             'sep': iris.Constraint(month_number=lambda cell: cell == 9),
             'oct': iris.Constraint(month_number=lambda cell: cell == 10),
             'nov': iris.Constraint(month_number=lambda cell: cell == 11),
             'dec': iris.Constraint(month_number=lambda cell: cell == 12),
             'djf': iris.Constraint(month_number=lambda cell: (cell == 12) | (1 <= cell <= 2)),
             'mam': iris.Constraint(month_number=lambda cell: 3 <= cell <= 5),
             'jja': iris.Constraint(month_number=lambda cell: 6 <= cell <= 8),
             'jas': iris.Constraint(month_number=lambda cell: 7 <= cell <= 9),
             'jjas': iris.Constraint(month_number=lambda cell: 6 <= cell <= 9),
             'mjjas': iris.Constraint(month_number=lambda cell: 5 <= cell <= 9),
             'son': iris.Constraint(month_number=lambda cell: 9 <= cell <= 11)
             }

    return (sncon[name])


if __name__ == "__getSeasConstr__":
    getSeasConstr(season)

############################################

def main(incube,season,ncfile):
    '''Calculates the total rain over the time period'''
    print 'This is the calc script: calc_mean_rain'

    slicer = getSeasConstr(season)
    iris.coord_categorisation.add_month_number(incube, 'time', name='month_number')
    iris.coord_categorisation.add_year(incube, 'time', name='year')

    incube = incube.extract(slicer)
    incube.convert_units('kg m-2 day-1')

    incube = incube.collapsed(['latitude', 'longitude'], iris.analysis.SUM)

    totrain = incube.aggregated_by(['year'], iris.analysis.SUM)
    wetdays = incube.aggregated_by(['year'], iris.analysis.COUNT,
                                   function=lambda values: values > 1.0)

    meanrain = totrain/wetdays

    iris.save(meanrain,ncfile)

if __name__ == "__main__":
	main(incube,season,ncfile)