'''
this is a code to create Hovmoller and time series plots from somme sample CMIP5
Autor: Oumar  KONTE, December 2016
'''
import os
import iris 
import iris.coord_categorisation
import iris.quickplot as qplt
import numpy as np
import matplotlib.pyplot as plt


def plotHovmoller(incube, figdir):
  '''
    Input
        -include : A 3D cube with time, lat and lon dimension (iris cube)
        -figdir : An output path to write the figure to (chr string).
    Output
        -a nice plot of the Hovmollert!
  '''


def main():
    # this function that controls everything
    figdir = '/nfs/see-fs-01_teaching/earv054/metrics_workshop/Ou_Ko/plot'
    try:
        cube2plot = iris.load_cube('hovmoller.nc')
        print cube2plot
        #plotHovmoller(mydata, figdir)
    except IOError:
        mycube = iris.load_cube('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/IPSL-CM5A-LR/historical/pr_WFDEI_1979-2013_0.5x0.5_day_IPSL-CM5A-LR_africa_historical_r1i1p1_full.nc')
        reg_cube = mycube.intersection(latitude=(4.0,25.0), longitude=(-10, 10.0))
        reg_cube.coord('latitude').guess_bounds()
        reg_cube.coord('longitude').guess_bounds()
        reg_cube_coll = reg_cube.collapsed('longitude', iris.analysis.MEAN)
        iris.coord_categorisation.add_month_number(reg_cube_coll, 'time', name='month')
        cube2plot =  reg_cube_coll.aggregated_by('month',iris.analysis.MEAN)      
        cube2plot.convert_units('kg m-2 day-1')
        plotHovmoller(cube2plot, figdir)
        iris.save(cube2plot, 'hovmoller.nc')
        print 'saved'
        
    my_level = np.linspace(1, 50, 10)
    plt.clf()
    qplt.contourf(cube2plot, levels=my_level, extend='max')
    plt.show()
   # plt.ylabel('Time / years')
  #  plt.axis('tight')
    #plt.gca().yaxis.set_major_locator(mdates.YearsLocator())  

if  __name__=='__main__':
    main()