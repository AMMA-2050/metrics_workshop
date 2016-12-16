'''
This is a code to create Monthly Temp, Season Temp, surface Tmax, 2m Tmax and Tmin from some plot CMIP5
Author: Siny NDOYE, December 2016
'''
import os
import iris
import iris.coord_categorisation
import iris.quickplot as qplt
import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt as gent
import mpl_toolkits.basemap as bm
from matplotlib import cm



def workshop_metrics_mean_temperature(Temp1, figdir):
    '''
    Inputs
     - incube : A 3D cube with time, lat and lon dimensions (iris cube)
     - figdir : An output path to write the figure to (chr string)
    Outputs
     - a nice plot of the huvmoller
    '''
    #levels=np.linspace(282,302,10)
    a = np.max(Temp1[:,:])
    b = np.min(Temp1[:,:])
    
    levels = np.linspace(np.amin(Temp1[:,:]),np.max(Temp1[:,:]) , 13)
    #print(levs)    
    print levels
    qplt.contourf(Temp1, levels = levels, extend = 'max')
    #fig1=qplt.contourf(Temp1, levels = levels, extend = 'max')
    #plt.clabel(fig1, inline=1)   #adds numbers to your contours
    m = bm.Basemap(projection='cyl', llcrnrlat=8.0, urcrnrlat=16.0, llcrnrlon=-20.0, urcrnrlon=20.0, resolution='c')  # coarse resolution for grid
    m.drawcoastlines(linewidth=2)
    m.drawcountries(linewidth=1)
    plt.savefig(figdir + 'Tmean.png' )
    plt.show()    
    
    
    
def main():
    figdir='/nfs/see-fs-01_teaching/earv053/metrics_workshop/plots/'
    infile = '/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/IPSL-CM5A-LR/historical/tas_WFDEI_1979-2013_0.5x0.5_day_IPSL-CM5A-LR_africa_historical_r1i1p1_full.nc'
    if os.path.isfile(infile):
        print "The file exists!"
    #mycube = mycube.intersection(latitude=(4, 25), longitude=(-10, 10)) # for example
    mycube = iris.load_cube(infile)
    print mycube
    print mycube[0][:,:]
    mycube.coord('latitude').guess_bounds()
    mycube.coord('longitude').guess_bounds()
    Temp=mycube
    #Temp.convert_units('Celsius') # convert unit 

    # choix du domaine
    Temp = Temp.intersection(latitude=(4.0, 25.0), longitude=(-18, 25.0))
    Temps=Temp
    #iris.coord_categorisation.add_month(Temp, 'time', name='month')
    iris.coord_categorisation.add_month_number(Temp, 'time', name='month')
    iris.coord_categorisation.add_season(Temps, 'time', name='clim_season', seasons=('djf', 'mam', 'jja', 'son'))

    #qplt.pcolormesh(Temp[1])
    #plt.show
    print Temp.coord('month')
    print Temp.coord('month').shape
    #compute the monthly value
    Tempm = Temp.aggregated_by('month', iris.analysis.MEAN)
    Tempss = Temps.aggregated_by('clim_season', iris.analysis.MEAN)
    # define min and max value
    #a = np.max(Tempm[:,:])
    #b = np.min(Tempm[:,:])
    
    #levs = np.linspace(np.amin(Tempm[:,:]), a, 13)
    #print(levs)
    # Open figure window
    #ax1 = plt.figure(figsize=(10, 15))

    #Tempm = Temp.aggregated_by('month', iris.analysis.MEAN)
    Temp1=Tempm[1]
    plt.subplot(3, 1, 1)
    workshop_metrics_mean_temperature(Temp1, figdir)  
    Temps1=Tempss[1]
    plt.subplot(3, 1, 2)
    workshop_metrics_mean_temperature(Temps1, figdir)
    plt.subplot(3, 1, 3)
    workshop_metrics_mean_temperature(Tempss[2], figdir)
    #plt.subplot(5, 1, 4)
    #workshop_metrics_mean_temperature(Tempss[3], figdir)   
    #plt.subplot(5, 1, 5)
    #workshop_metrics_mean_temperature(Tempss[4], figdir)
    
    iris.save(Tempm, str(figdir) + 'Tmean.nc')
    iris.save(Tempss, str(figdir) + 'TmeanS.nc')

    print(Tempm.shape)
    #print(Tempss.shape)

    #qplt.pcolormesh(Tempm[1])


    
if __name__== '__main__':
    main()    