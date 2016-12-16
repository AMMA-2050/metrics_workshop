''' 
cal_seasonal
This code is to calculate the seasonal mean of rainfall during JJAS
December 2016

'''
import iris
import matplotlib.pyplot as plt
import os
import iris.coord_categorisation
import numpy as np
import iris.quickplot as qplt
import mpl_toolkits.basemap as bm

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
            'son': iris.Constraint(month_number=lambda cell: 9 <= cell <= 11)
            }

    return(sncon[name])
    
def cal_seasonal(mycube, ncfile1, ncfile2):
        
    iris.coord_categorisation.add_month_number(mycube, 'time', name='month_number')
    iris.coord_categorisation.add_year(mycube, 'time', name='year')
    jjas_con = getSeasConstr('jjas')
    mycube_jjas = mycube.extract(jjas_con)
    #print mycube_jjas

    mycube_jjas.coord('latitude').guess_bounds()
    mycube_jjas.coord('longitude').guess_bounds()  
    mycube_jjas.convert_units('kg m-2 day-1')
    #mycube_jjas = mycube_jjas.collapsed(['longitude','latitude'],iris.analysis.MEAN)
    
    mycube_jjas2 = mycube_jjas
    mycube_jjas2 = mycube_jjas2.collapsed('year', iris.analysis.MEAN)
    print mycube_jjas2
    
    mycube_jjas = mycube_jjas.aggregated_by('year',iris.analysis.MEAN)
    mycube_jjas = mycube_jjas.collapsed('longitude', iris.analysis.MEAN)
    mycube_jjas = mycube_jjas.collapsed('latitude', iris.analysis.MEAN)

    
    iris.save(mycube_jjas, ncfile1)
    iris.save(mycube_jjas2, ncfile2)
       
    return([mycube_jjas, mycube_jjas2]) 
    
    