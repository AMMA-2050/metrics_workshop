#####################################
#
# contourf_no_map.py
#
#
# pass in:
#   incube - the cube to plot
#   what_am_i - th ncfile name to give a plot title
####################################

import iris
import matplotlib.pyplot as plt
import numpy as np

def main(incube,outpath,what_am_i):
    plt.clf()
    lon = incube.coord('month').points
    lat = incube.coord('latitude').points
    # find levels for the contours
    ranger = 0
    levs = []
    modelnums = incube.coord('model_name').points
    for t in modelnums:
        slicer = iris.Constraint(model_name = str(t))
        range_finder = incube.extract(slicer)
        range_finder = range_finder.data
        ranger_test = np.max(range_finder[:]) - np.min(range_finder[:])
        if ranger_test > ranger:
            ranger = ranger_test
            levs = np.linspace(np.min(range_finder[:]),np.max(range_finder[:]),20)
    # ace now we can plot
    cntr = 1
    for t in modelnums:
        plt.subplot(6,5,cntr+1)
        cntr = cntr + 1
        slicer = iris.Constraint(model_name = str(t))
        range_finder = incube.extract(slicer)
        range_finder = range_finder.data    
	print range_finder.shape, len(lon), len(lat)
        cd = plt.contourf(lat,lon,range_finder[:], levs, cmap = plt.get_cmap('spectral'))
        plt.title(str(t))
        if t == modelnums[-1]:
            cb = plt.colorbar(cd)
# need to find out how to grab the units of the cube from the cube            
    plt.suptitle(str(what_am_i))
    plt.savefig(str(outpath)+'/'+str(what_am_i)+'.png')
    print "Donezo"
    
if __name__ == "__main__":
    contourf_no_map(incube,outpath,what_am_i)            
