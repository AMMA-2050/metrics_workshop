##############################################################

#SCRIPT TO CALCULATE ANNUAL MAXIMUM

##############################################################
import itertools
import iris
import iris.coord_categorisation


def variable_setter(string):

        if string == 'var':
           string = 'pr'
        if string == 'plot_type':
           string = 'contourf_map'
        if string == 'seas':
           string = 'ann'
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
        This file calculates the annual maximum of
        a variable. It is preset to use precipitation,
        but can also use Temperature.
        '''
        print 'This is the calc script'


	iris.coord_categorisation.add_year(cubein,'time',name='year')
        iris.coord_categorisation.add_month_number(cubein,'time',name = 'month_number')

        slicer = getSeasConstr(season)
        cubein = cubein.extract(slicer)

        cube2plot = cubein
        if "pr_" in ncfile: 
	        cube2plot.convert_units('kg m-2 day-1')
        annmax = cube2plot.aggregated_by(['year'], iris.analysis.MAX)

        iris.save(annmax,ncfile)
        return(annmax)

    
if __name__ == '__main__': 
    main(cubein,season,ncfile)
    
