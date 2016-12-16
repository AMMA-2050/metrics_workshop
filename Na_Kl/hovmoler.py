import os
import matplotlib.pyplot as plt
import numpy as np
import iris
import iris.coord_categorisation
import iris.quickplot as qplt
#from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
from matplotlib.dates import MONTHLY

def plotHovmuller(incube, figdir):
    
    """
    put comment here
    Inputs
        -include: A 3D cube with time, lat and lon dimensions(iris cube)
        - figdir: An output path to write the figure to (chr string)
      Outputs  
        - a nice plot of the hovmuller!
    
    """
    plt.clf()
    print incube
    levels=np.linspace(1, 50, 10)
    #months = MonthLocator(range(1, 13), bymonthday=1, interval=1)
    #monthsFmt = DateFormatter("%b")

    qplt.contourf(incube, levels=levels, extend='max', cmap=plt.get_cmap('bwr'))
    #plt.xlim(0, 12)
    ax = plt.gca()
    #plt.plot_date(0,12)

    #loc = ax.xaxis.get_major_locator()
    #loc.maxticks[MONTHLY] = 12
    #ax.xaxis.set_major_locator(months)
    #ax.xaxis.set_major_formatter(monthsFmt)
    #plt.savefig(figdir+'hov.png')
    plt.show()
    
def main():
    # this is the function that controls everything 
    figdir='/nfs/see-fs-01_teaching/earv060/plots/'
    try:
        mydata=iris.load_cube(figdir+'hovmuller.nc')
        plotHovmuller(mydata,figdir)
    except IOError:
        my_cube = iris.load_cube('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/MIROC5/historical/pr_WFDEI_1979-2013_0.5x0.5_day_MIROC5_africa_historical_r1i1p1_full.nc')
        #print my_cube
    
        precip=my_cube.intersection(latitude=(4.0, 25.0), longitude=(-10.0, 10.0))
        #precip.convert_units('kg m-2 d-1')  # convert unit
        #print precip
        precip_coll = precip.collapsed('longitude', iris.analysis.MEAN)
        iris.coord_categorisation.add_month(precip_coll, 'time',name='month')
        cube2plot = precip_coll.aggregated_by('month', iris.analysis.MEAN)
        cube2plot.convert_units('kg m-2 day-1')
        iris.save(cube2plot,figdir+'hovmuller.nc')
        plotHovmuller(cube2plot,figdir)
        
        print 'saved'
    
if __name__ == '__main__': 
    main()
    
        
        
