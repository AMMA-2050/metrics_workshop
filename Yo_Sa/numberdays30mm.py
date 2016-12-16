"""
Calculating number days rain > 30 mm
==============================

"""
import os

import iris    #  handling cubes of big data
import iris.coord_categorisation  # allows you to add new coordinates to your data cube
import iris.plot as iplt # a quickplot option from the Iris package
import iris.quickplot as qplt

import matplotlib.pyplot as plt # the package doing the plotting
import datetime # handles dates

import cartopy  # helps to create maps
import cartopy.crs as ccrs # helps to create maps
import numpy as np  # handles arrays
import mpl_toolkits.basemap as bm


def count_spells(data, threshold, axis, spell_length):
    '''
    '''

def main():
     figdir = '/nfs/see-fs-01_teaching/earv052/metrics_workshop/Yo_Sa'
     try:
        cube2plot = iris.load_cube(figdir+'/Leeds_numberdays30mm.nc')
        print cube2plot
     except IOError: 
        cube = iris.load_cube('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/IPSL-CM5A-LR/historical/pr_WFDEI_1979-2013_0.5x0.5_day_IPSL-CM5A-LR_africa_historical_r1i1p1_full.nc')
        precip = cube[0]
        #print(precip)
        precip = cube.intersection(longitude=(-18.0, 0.0), latitude=(10.0, 20.0))
        precip.coord('latitude').guess_bounds()
        precip.coord('longitude').guess_bounds()
        precip.convert_units('kg m-2 day-1')
        #print(precip)
        iris.coord_categorisation.add_month_number(precip, 'time', name='month')
        print(precip)
        #iris.coord_categorisation.add_day_of_year(precip, 'time', name='day_of_year')
        #ann_long = np.unique(precip.coord('year').points)
        #ann = len(ann_long)
        val=30.0
        bigger = precip.aggregated_by('month', iris.analysis.COUNT, function = lambda values: values > val )
        monthcount = precip.aggregated_by('month', iris.analysis.COUNT, function = lambda values: values > -5000)
        monthcount.data = monthcount.data.astype(float)
        print bigger
        print monthcount.data
        aug = bigger/monthcount
      #  aug = bigger.extract(iris.Constraint(month=8))/monthcount.extract(iris.Constraint(month=8))
        print aug.data
        qplt.contourf(aug.extract(iris.Constraint(month=8)))
##        qplt.contourf(bigger.extract(iris.Constraint(month=8)))
        #d = plt.gca() # get axis object
        #d.coastlines() # to draw coastlines
        m = bm.Basemap(projection='cyl', llcrnrlat=10.0, urcrnrlat=20.0, llcrnrlon=-18.0, urcrnrlon=0.0, resolution='c')  # coarse resolution for grid
        m.drawcoastlines(linewidth=2)
        m.drawcountries(linewidth=2)
        plt.show()

if __name__ == '__main__':
    main()
