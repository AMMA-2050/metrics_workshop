'''
calc_rainfallsequences10.py
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
Write one line describing the code here
'''
#In this part of the script, put your main
#metric calculation work.
#Some example lines of code that you may
#want to use are included below.
#
        if axis < 0:
        # just cope with negative axis numbers
        axis += data.ndim
        # Threshold the data to find the 'significant' points.
        data_hits = data > threshold
        # Make an array with data values "windowed" along the time axis.
        hit_windows = iris.util.rolling_window(data_hits, window=rain_length, axis=axis)
        # Find the windows "full of True-s" (along the added 'window axis').
        full_windows = np.all(hit_windows, axis=axis+1)
        # Count points fulfilling the condition (along the time axis).
        rain_point_counts = np.sum(full_windows, axis=axis, dtype=int)
        return rain_point_counts

        iris.coord_categorisation.add_month_number(cubein,'time',name = 'month_number')
        iris.coord_categorisation.add_year(cubein,'time',name='year')
        iris.coord_categorisation.add_day_of_year(cubein,'time',name='day_of_year')
        slicer = getSeasConstr(season)
        cubein = cubein.extract(slicer)
#
        cube2plot = cubein
        cube2plot.convert_units('kg m-2 day-1')     
        
#        yrs = cube2plot.aggregated_by('year',iris.analysis.MEAN)
        
#Start computation of rain days
    # Make an aggregator from rain days count
        count = iris.analysis.Aggregator('rain_count',count_spells,
                                 units_func=lambda units: 1)

# Define the parameters
        thresh_rain = 1
        rain_days = 10

# Calculate the statistic
        rain_days10 = pcp.collapsed('time', count,threshold=thresh_rain,
                                      rain_length=rain_days)
        rain_days.rename('Number of days with rain > 1mm day-1 over 10 consecutive days')


	iris.save(rain_days10,ncfile)


if __name__ == "__main__":
	main(cubein,season,ncfile)
