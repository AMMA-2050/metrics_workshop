'''
This is code to create hovmoller and timeseries plots from some sample CMIP5 data
Author: Andy Hartley, December 2016
'''
import os
import iris
import iris.coord_categorisation
import iris.quickplot as qplt
import numpy as np
import matplotlib.pyplot as plt


def hello(name):
    print name + ' is a big Leeds United fan'
    

def plotHovmoller(incube, figdir):
    '''
    Inputs
        - incube : A 3D cube with time, lat and lon dimensions (iris cube)
        - figdir : An output path to write the figure to (chr string)
    Ouputs
        - a nice plot of the hovmoller!
    '''
    levels = np.arange(1,15,1)
    print levels
    plt.clf()
    qplt.contourf(incube, levels = levels, extend = 'max')
    plt.savefig(figdir + 'hovmoller.png')
    plt.show()
    
def main():
    # This the function that controls everything

    figdir = '/nfs/see-fs-01_teaching/earv061/plots/'
    try:        
        mydata = iris.load_cube(str(figdir)+'hovmoller.nc')
        plotHovmoller(mydata,figdir)        
    except IOError:    
        mycube = iris.load_cube('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/IPSL-CM5A-LR/historical/pr_WFDEI_1979-2013_0.5x0.5_day_IPSL-CM5A-LR_africa_historical_r1i1p1_full.nc')
        reg_cube = mycube.intersection(latitude=(4, 25), longitude=(-10, 10))
        reg_cube.coord('latitude').guess_bounds()
        reg_cube.coord('longitude').guess_bounds()    
        reg_cube_coll = reg_cube.collapsed('longitude', iris.analysis.MEAN)    
    #iris.coord_categorisation.add_day_of_year(reg_cube_coll, 'time', name='day_of_year')
        iris.coord_categorisation.add_month_number(reg_cube_coll, 'time', name='month')
    #cube2plot = reg_cube_coll.aggregated_by('day_of_year', iris.analysis.MEAN)
        cube2plot = reg_cube_coll.aggregated_by('month', iris.analysis.MEAN)
        cube2plot.convert_units('kg m-2 day-1')        
        plotHovmoller(cube2plot, figdir)        
        iris.save(cube2plot,str(figdir)+'hovmoller.nc')
        print 'saved'

    
    
if __name__ == '__main__':
    main()
