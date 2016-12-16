'''
this is a code to create hovmoller and timeseries plots from sample CMIP5
Author: Adama Bamba December 2016
'''
import os
import iris
import iris.coord_categorisation
import iris.quickplot as qplt
import numpy as np
import matplotlib.pyplot as plt



def plotHovmoller(incube, figdir):
    '''
    inputs
        - incube : A 3D cube with time, lat and lon dimension
        - figdir : An output path to write the figure to
        outpus
        - a nice a plot of the hovmoller!
    '''
    
def main():
    # This is the function that controls everthing
    figdir = '/nfs/see-fs-01_teaching/earv056/metrics_workshop/Ad_Ba/my_plots'
    try:
       var2plot = iris.load_cube('I_like_leeds.nc') 
#       plotHovmoller(my_cube, figdir)
       print var2plot
    except IOError:
       my_cube = iris.load_cube('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/HadGEM2-ES/historical/pr_WFDEI_1979-2013_0.5x0.5_day_HadGEM2-ES_africa_historical_r1i1p1_full.nc')        
       reg_cube = my_cube.intersection(longitude=(-10.0, 10.0), latitude=(4.0, 26.0))
       reg_cube.coord('latitude').guess_bounds()
       reg_cube.coord('longitude').guess_bounds()
       reg_cube_coll = reg_cube.collapsed('longitude', iris.analysis.MEAN)
       iris.coord_categorisation.add_day_of_year(reg_cube_coll, 'time', name='day_of_year')
       var2plot = reg_cube_coll.aggregated_by('day_of_year', iris.analysis.MEAN)
       var2plot.convert_units('kg m-2 day-1')
       plotHovmoller(var2plot, figdir)
    

       iris.save(var2plot,'I_like_leeds.nc')
    #levels = np.arange(1, 20)
    levels = np.linspace(1,20,20)
    plt.clf()
    print levels
    qplt.contourf(var2plot, levels = levels, extend = 'max')
      #qplt.contourf(var2plot, 20)
    plt.savefig(figdir + 'hovmoller.png')
    plt.show()
    print 'saved'
    
    
if __name__== '__main__':
    main()