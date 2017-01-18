#####################################
#
# contourf_map.py
#
#
# pass in:
#   incube - the cube to plot
#   what_am_i - th ncfile name to give a plot title
####################################

import iris
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as bm
import numpy as np

def main(incube,outpath,what_am_i):
    plt.clf()
    # find boundaries for map
    x1 = incube.coord('longitude').points[0]
    x2 = incube.coord('longitude').points[-1]
    y1 = incube.coord('latitude').points[0]
    y2 = incube.coord('latitude').points[-1]
    lon = incube.coord('longitude').points
    lat = incube.coord('latitude').points
    # find levels for the contours
    ranger = 0
    levs = []
    modelnums = incube.coord('model_name').points
    for t in modelnums:
        slicer = iris.Constraint(model_name = str(t))
        range_finder = incube.extract(slicer)
        range_finder = range_finder.data
        ranger_test = np.max(range_finder[:]) - np.nanmin(range_finder[:])
        if ranger_test > ranger:
            ranger = ranger_test
            levs = np.linspace(np.min(range_finder[:]),np.max(range_finder[:]),20)

    print levs[:]	
    # ace now we can plot
    cntr = 1
    for t in modelnums:
        plt.subplot(6,5,cntr+1)
        cntr = cntr + 1
        slicer = iris.Constraint(model_name = str(t))
        range_finder = incube.extract(slicer)
        print range_finder
        range_finder = range_finder.data    
        m = bm.Basemap(projection='cyl',llcrnrlat = y1, urcrnrlat = y2, llcrnrlon = x1, urcrnrlon = x2,  resolution = 'c') 
        m.drawcoastlines()
        m.drawcountries()
        cd = plt.contourf(lon,lat,range_finder[0,:,:], levs, cmap = plt.get_cmap('spectral'))
        plt.title(str(t))
        if t == modelnums[-1]:
            cb = plt.colorbar(cd,orientation ='horizontal')
# need to find out how to grab the units of the cube from the cube            
    plt.suptitle(str(what_am_i))
    plt.savefig(str(outpath)+'/'+str(what_am_i)+'.png')
    plt.show()
 
if __name__ == "__main__":
    contourf_map(incube,outpath,what_am_i)            
