'''
This is a code to create a hovmoller and temeseries plots from CMIP5 data

Author: Youssouph Sane, Leeds at December 2016
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
      - incube: A 3D cube with time, lat and lon dimensions (iris cube)
      - figdir: An output path to write the figure to (chr string) Output
      - a nice plot of hovmoller
    '''
    
def main():
    figdir = '/nfs/see-fs-01_teaching/earv052/metrics_workshop/Yo_Sa'
    try:
        cube2plot = iris.load_cube(figdir+'/Leeds_is_great.nc')
        print cube2plot
    except IOError: 
        cube = iris.load_cube('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/IPSL-CM5A-LR/historical/pr_WFDEI_1979-2013_0.5x0.5_day_IPSL-CM5A-LR_africa_historical_r1i1p1_full.nc')
        precip = cube.intersection(longitude=(-18.0, -12.0), latitude=(12.0, 18.0))
        precip.coord('latitude').guess_bounds()
        precip.coord('longitude').guess_bounds()
        hov = precip.collapsed('longitude', iris.analysis.MEAN)
        iris.coord_categorisation.add_month_number(hov, 'time', name='month')
        cube2plot = hov.aggregated_by('month',iris.analysis.MEAN)
        cube2plot.convert_units('kg m-2 day-1')
        plotHovmoller(cube2plot, figdir)
        iris.save(cube2plot,figdir+'/Leeds_is_great.nc')
        print 'saved'     
    levels = np.linspace(1,50,10)
    print cube2plot
    cube2plot.convert_units('kg m-2 day-1')    
    print levels
    plt.clf()
    qplt.contourf(cube2plot, levels=levels, extend = 'max')     
    plt.show()
           
if __name__ == '__main__':
    main()