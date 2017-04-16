'''
calc_numberdays30mm.py
'''

import iris
import numpy as np
import scipy as sci
import matplotlib.pyplot as plt
import iris.coord_categorisation

def variable_setter(string):

	if string == 'var':
           string = 'pr'
	if string == 'plot_type':
	   string = 'contourf_map'
	if string == 'seas':
	   string = 'mjjas'
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
    Write something here to describe the file
    '''
    print "This is the calc script"
    iris.coord_categorisation.add_month_number(cubein, 'time', name='month_number')
    iris.coord_categorisation.add_year(cubein,'time',name='year')
    slicer = getSeasConstr(season)
    print "This is the cubein"
    print cubein
    cube2plot = cubein.extract(slicer)
    print "This is the cube2plot"
    print cube2plot
#    cubein = cubein.extract(slicer)
# You do not need to do cubein.intersection here. This is done in the load data script
# Instead, when you use ultimo_burrito, make a custom region with these boundaries
#    cube2plot = cubein.intersection(longitude=(-20.0, -11.0), latitude=(12.0, 20.0))
    cube2plot.coord('latitude').guess_bounds()
    cube2plot.coord('longitude').guess_bounds()
    cube2plot.convert_units('kg m-2 day-1')
    yrs = cube2plot.aggregated_by('year',iris.analysis.MEAN)
    empty = yrs.data
    years = yrs.coord('year').points
    dates = []
    val=30.0

    for yr in years: #loop through the years
           # so you have sliced the data here. 
           yrslice = iris.Constraint(year = lambda cell: cell == yr)
           N5 = cube2plot.extract(yrslice)
    # So, at this point are you trying to aggregate by month?
    # If you just wanted to do this for every year, you do not need half of this.
    # If you just want a count for every year, delete the for yr in years loop and change the aggregated_by to what I have commented out.
    # otherwise, these need to be in the loop...       
#    bigger = cube2plot.aggregated_by('year', iris.analysis.COUNT, function = lambda values: values > val )
#    monthcount = cube2plot.aggregated_by('year', iris.analysis.COUNT, function = lambda values: values > -5000)

    bigger = N5.aggregated_by('month_number', iris.analysis.COUNT, function = lambda values: values > val )
    monthcount = N5.aggregated_by('month_number', iris.analysis.COUNT, function = lambda values: values > -5000)
    monthcount.data = monthcount.data.astype(float)
    numdays30mm = (bigger/monthcount)*100

    iris.save(numdays30mm,ncfile)
    

if __name__ == "__main__":
        main(cubein,season,ncfile)
