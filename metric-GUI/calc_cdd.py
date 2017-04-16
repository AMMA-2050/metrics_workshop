'''
calc_cdd.py
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

        iris.coord_categorisation.add_day_of_month(cubein, 'time', name='day_of_month')
        iris.coord_categorisation.add_season_year(cubein, 'time', name='season_year', seasons=('djf', 'mam', 'jja', 'son'))
        cubein.convert_units('kg m-2 day-1')
        outcube = cubein.aggregated_by('season_year', iris.analysis.MEAN)
    #the rainfall threshold
        total = 1.0
    # first bring in the data
    # this code will need to know the starting day of the data
        for yr in cubein.coord('season_year').points:
        #pdb.set_trace()
            incube_yr = cubein.extract(iris.Constraint(season_year=yr))
        
            strt_day = incube_yr.coord('day_of_month').points[0]   
            yeardata = incube_yr.data
# We do not need these as we will not be working with lists
#        dtes = []
#        duration = []

# you will need to check that the bolw line works. We are collapsing the 3d
# file in to 2 dimensions
            yearcoll = incube_yr.collapsed ('season_year', iris.analysis.MEAN)
       # yearcoll = incube_yr.collapsed('season_year')
        
# then we will have 2 identical cubes we fill the data in to
            pltdtes = yearcoll
            pltdur = yearcoll   

            for x in range(0,yeardata.shape[2]):
                for y in range(0,yeardata.shape[1]):
                    current_max = 0
                    current_dte = 0
                    dte = 0
                    duratn = 0   
                    for t in range(0,yeardata.shape[0]):
                        if yeardata[t,y,x] <= float(total):
                           dte = t
                           print dte, yeardata[t,y,x]
                           for t1 in xrange(t,yeardata.shape[0]): 
                               if yeardata[t1,y,x] <= float(total):
                                  continue
                               else:
                                       duratn = t1 - t
                                       if duratn > current_max:
                                         current_dte = dte + strt_day
                                         current_max = duratn
                               break
                pltdtes[y,x].data = current_dte
                pltdur[y,x].data = current_max

        outpath = '/home/dem/Bureau/'
        iris.save(pltdtes,outpath+'ccd_dates.nc')
        iris.save(pltdur,outpath+'ccd_dur.nc')
        
        return(pltdtes,pltdur)
        
    # so right now you are not saving the right files. You want to save pltdtes
    # and pltdur
        iris.save(outcube,outfile) 
          
if __name__ == "__main__":
	main(cubein,season,ncfile)
