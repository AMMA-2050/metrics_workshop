''' 
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
    
def plot(infile, figpath):
    # this 
    print infile
   
def main():
    # path ='/nfs/a266/data/CMIP5_AFRICA/0.5x0.5/CanESM2/historical/'
    # iris.load_cube(path)
    infile = '/nfs/a266/data/CMIP5_AFRICA/0.5x0.5/CanESM2/historical/pr_day_CanESM2_africa_0.5x0.5_historical_r1i1p1_full.nc'
    mycube = iris.load_cube(infile)
    mycube.intersection(latitude = (0,25),longitude = (-20,20))
   # print mycube
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

    #mycube_jjas2= iris.coords.Coord(mycube_jjas, month='month_number') 
    
    print mycube_jjas
    #annual_seasonal_mean = mycube.aggregated_by(['clim_season', 'season_year'],iris.analysis.MEAN)
    #years = np.linspace(0,56,56)
    years = np.linspace(0,len(mycube_jjas.data),len(mycube_jjas.data))
    
    f = plt.figure(figsize=(6, 6))
    
    plt.subplot(2, 1, 1)
    
    plt.bar(years, mycube_jjas.data[:])
    plt.xlabel('years')
    plt.ylabel('precip kg m-2 day-1')
    plt.xlim(0, len(mycube_jjas.data))
    plt.suptitle('JJAS precipitation over West Africa 0-25N and 20W-20E')
    
    plt.subplot(2, 1, 2)       
    levs = np.linspace(1,20,20)
    qplt.contourf(mycube_jjas2, levs)
    m = bm.Basemap(projection='cyl', llcrnrlat=0.0, urcrnrlat=20.0, llcrnrlon=-20.0, urcrnrlon=20.0, resolution='c') # medium resolution for grid
    m.drawcoastlines(linewidth=2)
    m.drawcountries(linewidth=1)
    #qplt.pcolor(mycube_jjas2)
    plt.show()
    #print annual_seasonal_mean
    
if __name__ == '__main__':
    main()