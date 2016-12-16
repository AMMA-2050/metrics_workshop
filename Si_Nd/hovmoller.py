'''
This is a code to create hovmoller and timeseries plot from some plot CMIP5
Author: Siny NDOYE, December 2016
'''
import os
import iris
import iris.coord_categorisation
import iris.quickplot as qplt
import numpy as np
import matplotlib.pyplot as plt

def hello(name):
    print name + 'is a bgi Leeds United fan'

def plotHuvmoller(incube, figdir):
    '''
    Inputs
     - incube : A 3D cube with time, lat and lon dimensions (iris cube)
     - figdir : An output path to write the figure to (chr string)
    Outputs
     - a nice plot of the huvmoller
    '''
    levels=np.linspace(1,15,20)
    print levels
    qplt.contourf(incube, levels = levels, extend = 'max')
    plt.savefig(figdir + 'hovmoller.png' )
    plt.show()
def main():
    figdir='/nfs/see-fs-01_teaching/earv053/metrics_workshop/plots/'
    try:
        mydata=iris.load_cube(str(figdir)+'hovmoller.nc')
        plotHuvmoller(mydata, figdir)
    except IOError:
        
        # this the function that control everything
        #print 'Hello from the main function
        figdir='/nfs/see-fs-01_teaching/earv053/metrics_workshop/plots/'
        mycube = iris.load_cube('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/IPSL-CM5A-LR/historical/pr_WFDEI_1979-2013_0.5x0.5_day_IPSL-CM5A-LR_africa_historical_r1i1p1_full.nc')
        print mycube
        reg_cube = mycube.intersection(latitude=(4, 25), longitude=(-10, 10))
        reg_cube.coord('latitude').guess_bounds()
        reg_cube.coord('longitude').guess_bounds()
    
        reg_cull_coll = reg_cube.collapsed('longitude', iris.analysis.MEAN)
    
        iris.coord_categorisation.add_month_number(reg_cull_coll, 'time', name='month')
        cube2plot = reg_cull_coll.aggregated_by('month', iris.analysis.MEAN)
        #levels = np
        cube2plot.convert_units('kg m-2 day-1')
    
        plotHuvmoller(cube2plot, figdir)
        iris.save(cube2plot, str(figdir) + 'hovmoller.nc')
        print 'saved'
        
    
    # Take the mean over latitude
    #mycube = mycube.collapsed('longitude', iris.analysis.MEAN)
    #print mycube
    #qplt.contourf(mycube,20)

    
if __name__== '__main__':
    main()
