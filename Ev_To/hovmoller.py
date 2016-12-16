'''
This is a code to create hovmoller and timeseries from sample CMIP5
Author:N'Datchoh E. T December 2016
'''
import os
import iris
import iris.coord_categorisation
import iris.quickplot as qplt
import numpy as np
import matplotlib.pyplot as plt


def plotHovmoller(incube, figdir):
    '''
    Inputs
    -incube: A 3D cube with time, lat and lon dimensions.
    -figdir: An output path to write the figure to
    Ouputs
    -a folder of Hovmoller plots will be placed!
    '''
def main():
    # This is a function that controls everything
#    mycube = iris.load_cube('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/HadGEM2-CC/rcp45/pr_WFDEI_1979-2013_0.5x0.5_day_HadGEM2-CC_africa_rcp45_r1i1p1_full.nc')
   
    figdir = '/nfs/see-fs-01_teaching/earv057/plots'
    try:
        cube2plot = iris.load_cube(figdir+'hovmoller.nc')
        print cube2plot
    except IOError:
        mycube = iris.load_cube('/nfs/a266/data/CMIP5_AFRICA/0.5x0.5/CanESM2/historical/pr_day_CanESM2_africa_0.5x0.5_historical_r1i1p1_full.nc')
        print mycube.coord('time').points[0:40]   
        reg_cube = mycube.intersection(latitude=(4,25), longitude=(-10,10))
        reg_cube.coord('latitude').guess_bounds()
        reg_cube.coord('longitude').guess_bounds()
        reg_cube_coll = reg_cube.collapsed('longitude', iris.analysis.MEAN) 
        iris.coord_categorisation.add_month(reg_cube_coll,'time', name ='month')
        cube2plot = reg_cube_coll.aggregated_by('month', iris.analysis.MEAN)
        cube2plot.convert_units('kg m-2 day-1')
        print cube2plot
        iris.save(cube2plot,figdir+'hovmoller.nc')
        print reg_cube_coll.coord('time')
#    print reg_cube_coll
#    print reg_cube_coll[0]
#    iris.coord_categorisation.add_day_of_year(reg_cube_coll, 'time', name = 'day_of_year')
    
    
    # partition
    #mycube = mycube.collapsed('longitude', iris.analysis.MEAN) 
#    print mycube
    levels = np.linspace(1,20,50)
    plt.clf()
    qplt.contourf(cube2plot, levels=levels, extend='max')
    plt.ylabel('latitude')   
    plt.xlabel('time/months')   
    plt.show()
if __name__ == '__main__':
    main()