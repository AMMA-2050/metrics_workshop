'''
calc_SJ.py
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
	   string = 'scatter'
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
	So in this file, we want to calculate the
	time when onset occurs. I.e when the precip
	at 10N is greater than precip at 5N for at least a week
	'''
	print 'This is the calc script'
#        print cubein
        iris.coord_categorisation.add_month_number(cubein,'time',name = 'month_number')
        iris.coord_categorisation.add_year(cubein,'time',name='year')
        slicer = getSeasConstr(season)
        cubein = cubein.extract(slicer)

        reg_cube_coll = cubein.collapsed('longitude', iris.analysis.MEAN)    
        cube2plot = reg_cube_coll
        cube2plot.convert_units('kg m-2 day-1')     
        
	#ok now calculate the date
        #first we want to know what years we have
        yrs = cube2plot.aggregated_by('year',iris.analysis.MEAN)
        yrscoll = yrs.collapsed('latitude',iris.analysis.MEAN)
	print yrs
        years = yrs.coord('year').points
        dates = []
        for yr in years:
#           print 'The year is'+str(yr)
#           this_year = cube2plot.intersection('year' = yr)
           yrslice = iris.Constraint(year = lambda cell: cell == yr)
           N5 = cube2plot.intersection(latitude = (4,6))
           N5coll = N5.collapsed('latitude',iris.analysis.MEAN)
           N5 = N5coll.extract(yrslice)
#           print N5
           N10 = cube2plot.intersection(latitude = (9,11))
           N10coll = N10.collapsed('latitude',iris.analysis.MEAN)
           N10 = N10coll.extract(yrslice)
           N5 = N5.data
           N10 = N10.data
           goodun = 500
           for t in range(0,N5.shape[0]-7):
              if np.average(N5[t:t+7]) <= np.average(N10[t:t+7]):
#                 dates.extend([119+t])
                 goodun = t+150
              else:
                continue
           
           dates.extend([goodun])
	yrscoll.data = dates[:] 

#        csvfile = ncfile.split('.')[0]
#        print csvfile, dates
#        np.savetxt(csvfile+'_onset_dates.csv', dates, delimiter = ',') 
#        np.savetxt(csvfile+'_years.csv',years, delimiter = ',')
#        return cube2plot, dates
	print yrscoll.data
        iris.save(yrscoll,ncfile)






if __name__ == "__main__":
	main(cubein,season,ncfile)
