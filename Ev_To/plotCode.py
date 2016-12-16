'''
 plotCode
 this code plot the seasonal calculation variables
 December 2016
 '''
 
import iris
import matplotlib.pyplot as plt
import os
import iris.coord_categorisation
import numpy as np
import iris.plot as iplt
import mpl_toolkits.basemap as bm
import cal_seasonal
import pdb

#climatology = iris.load_cube('/nfs/see-fs-01_teaching/earv057/ACCESS1-3_wafrica.climatology.nc')
#timeseries = iris.load_cube('/nfs/see-fs-01_teaching/earv057/ACCESS1-3_wafrica.timeseries.nc')

def plotCode(timeseries,climatology, modelID):
    
    years =timeseries.coord('year').points
    f = plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 2, 1)    
    plt.bar(years, timeseries.data)
    plt.xlabel('years')
    plt.ylabel('precip kg m-2 day-1')
    #plt.xlim(0, len(timeseries.data))
    plt.title('JJAS pr 5S-20N ; 18W-15E: '+modelID)
    
    plt.subplot(1, 2, 2)       
    levs = np.linspace(1,20,20)
    iplt.contourf(climatology, levs, cmap ='jet_r')
    m = bm.Basemap(projection='cyl', llcrnrlat=np.min(climatology.coord('latitude').points), urcrnrlat=np.max(climatology.coord('latitude').points), llcrnrlon=np.min(climatology.coord('longitude').points), urcrnrlon=np.max(climatology.coord('longitude').points), resolution='c') # medium resolution for grid
    m.drawcoastlines(linewidth=2)
    m.drawcountries(linewidth=1)
    plt.title('JJAS mean pr (1950-2005) 5S-20N ; 18W-15E:' +modelID)
    cbar = plt.colorbar(orientation="vertical")
    cbar.set_label('precip kg m-2 day-1')
    #qplt.pcolor(climatology)
    #plt.tight_layout()
    plt.savefig('/nfs/see-fs-01_teaching/earv057/metrics_workshop/Ev_To/Figures_png/'+modelID+'jjas.png')
    #plt.show()
    