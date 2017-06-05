'''
calc_Marteau_onset.py
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
	So in this file, we want to calculate the
	time when onset occurs. I.e when the precip
	at 10N is greater than precip at 5N for at least a week
	'''
	print 'This is the calc script'
#        print cubein
        iris.coord_categorisation.add_month_number(cubein,'time',name = 'month_number')
        iris.coord_categorisation.add_year(cubein,'time',name='year')
        iris.coord_categorisation.add_day_of_year(cubein,'time',name='day_of_year')
        slicer = getSeasConstr(season)
        cubein = cubein.extract(slicer)

        cube2plot = cubein
        cube2plot.convert_units('kg m-2 day-1')     
        
	#ok now calculate the date
        #first we want to know what years we have
        yrs = cube2plot.aggregated_by('year',iris.analysis.MEAN)
	empty = yrs.data
        years = yrs.coord('year').points
        dates = []
        tester = 14
        onsets = np.zeros((empty.shape[0],empty.shape[1],empty.shape[2]),float)
#        onsets = onsets.collapsed('year',iris.analysis.MEAN)
        for yr in years:
           yrslice = iris.Constraint(year = lambda cell: cell == yr)
           holdr = cubein.extract(yrslice)
           strt_date = holdr.coord('day_of_year').points[0]
           holdr = holdr.data   
	   for x in range(0,holdr.shape[2]):
     	      for y in range(0,holdr.shape[1]): 
	         latmean = 0
                 cnt0 = 0
                 A = 0
                 B = 0
                 C = 0
                 for t in xrange(0, holdr.shape[0] - tester-6):
			if holdr[t,y,x] > 1.0:
                           A4 = 1
                        else:
                           A4 = 0
                        if holdr[t+1,y,x] + holdr[t,y,x]> 20.0: 
                             A1 = 1
                        else:
                             A1 = 0
                        A2 = 1
                        t2 = 2
                        while t2 < tester-6:
                          drytest = holdr[t+t2,y,x] + holdr[t+t2+1,y,x] + holdr[t+t2+2,y,x] + holdr[t+t2+3,y,x] + holdr[t+t2+4,y,x] + holdr[t+t2+5,y,x]+holdr[t+t2+6,y,x]
                          if drytest < 5.0:
                             A2 = 0
                             break
                          else:
                             t2 = t2+1
                        A3 = A4+A2+A1
                        if A3 == 3:
		                  latmean =  t+strt_date
#		                  print 'Success', latmean
#				  onsets[yr-years[0],y,x].data = 27
 		                  onsets[yr-years[0],y,x] = latmean
			#	  print onsets[yr-years[0],y,x], latmean, yr-years[0]	
      				  break
                        else:
                         continue
                        break
                 if latmean== 0: 
                    onsets[yr-years[0],y,x] = float('NaN')
#                 onsets[y,x] = -100
                 




#	print onsets[:].data
	yrs.data = onsets[:]
	print yrs.data
        print strt_date
        iris.save(yrs,ncfile)






if __name__ == "__main__":
	main(cubein,season,ncfile)
