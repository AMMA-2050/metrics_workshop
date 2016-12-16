import os
import matplotlib.pyplot as plt
import numpy as np
import iris
import iris.plot as iplt
import iris.quickplot as qplt
import mpl_toolkits.basemap as bm
import pdb
#from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter

   
def main():
    # this is the function that controls everything 
    figdir='/nfs/a266/earv060/wetdays/'
    try:
        mydata=iris.load_cube(figdir+'cwd.nc')
        plotcwd(my_cube,figdir)
    except IOError:
        my_cube = iris.load_cube('/nfs/a266/earv060/wetdays/meanwetdays_permonth.nc')       
        #iplt.pcolormesh(my_cube[0,:,:])
         # make subplots of j j a
        plt.subplot(4, 1, 1)
        qplt.contourf(my_cube[5,:,:])
        plt.title('June')
        plt.grid(True)
        plt.subplots_adjust(hspace=0.4)
        m = bm.Basemap(projection='cyl', llcrnrlat=2.0, urcrnrlat=12.0, llcrnrlon=-20.0, urcrnrlon=20.0, resolution='f') # fine resolution for grid
        m.drawcoastlines(linewidth=2)
        m.drawcountries(linewidth=1)
        #d = plt.gca() # get axis object
        #d.coastlines() # to draw coastlines
        #d.countries(linewidth=1)
        
        plt.subplot(4, 1, 2)
        qplt.contourf(my_cube[6,:,:])
        plt.title('July')
        plt.grid(True)
        m = bm.Basemap(projection='cyl', llcrnrlat=2.0, urcrnrlat=12.0, llcrnrlon=-20.0, urcrnrlon=20.0, resolution='f') # fine resolution for grid
        m.drawcoastlines(linewidth=2)
        m.drawcountries(linewidth=1)
        
        plt.subplot(4, 1, 3)
        qplt.contourf(my_cube[7,:,:])
        plt.title('August')
        plt.grid(True)
        m = bm.Basemap(projection='cyl', llcrnrlat=2.0, urcrnrlat=12.0, llcrnrlon=-20.0, urcrnrlon=20.0, resolution='f') # fine resolution for grid
        m.drawcoastlines(linewidth=2)
        m.drawcountries(linewidth=1)
                
        my_scube = iris.load_cube('/nfs/a266/earv060/wetdays/meanwetdays_perseason1.nc')
        #add mean jja 
        plt.subplot(4, 1, 4)
        qplt.contourf(my_scube[0,:,:])
        plt.title('JJA')
        plt.grid(True)
        m = bm.Basemap(projection='cyl', llcrnrlat=2.0, urcrnrlat=12.0, llcrnrlon=-20.0, urcrnrlon=20.0, resolution='f') # fine resolution for grid
        m.drawcoastlines(linewidth=2)
        m.drawcountries(linewidth=1)
        
        plt.subplots_adjust(hspace=0.4)
        plt.show()
        #print my_scube.shape
    
if __name__ == '__main__': 
    main()
    
        