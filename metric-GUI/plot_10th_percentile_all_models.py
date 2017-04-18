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
import make_big_anomaly

def main(incube,outpath,what_am_i,sc,file_searcher):

    # so the first thing we want to do here is use anomalies and not raw data
    # BUT WE ONLY WANT TO DO THIS IF WE ARE USING AN RCP scenario!
    if "rcp" in sc:
       print 'rcp in scenario'
       bigcube = make_big_anomaly.main(incube,file_searcher,sc)

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
#    print incube.shape
    percentiles = incube.collapsed('model_name', iris.analysis.PERCENTILE, percent=[ 10,90])
#    iris.coord_categorisation.add_year(percentiles, 'time', name = 'year')
#    averages = percentiles.collapsed('year', iris.analysis.MEDIAN)
    print percentiles
    plt.clf()
    plt.subplot(2,1,1)
    m = bm.Basemap(projection='cyl',llcrnrlat = y1, urcrnrlat = y2, llcrnrlon = x1, urcrnrlon = x2,  resolution = 'l')
    m.drawcoastlines(linewidth= 2)
    m.drawcountries(linewidth = 1)     
    cd = plt.contourf(lon,lat,percentiles[0,:,:].data)
    cb = plt.colorbar(cd, orientation = 'horizontal')
    plt.text(float(x1) - 1., float(y2) - 1., '(a)')
    plt.subplot(2,1,2)
    m = bm.Basemap(projection='cyl',llcrnrlat = y1, urcrnrlat = y2, llcrnrlon = x1, urcrnrlon = x2,  resolution = 'l')
    m.drawcoastlines(linewidth= 2)
    m.drawcountries(linewidth = 1)     
    cd = plt.contourf(lon,lat,percentiles[1,:,:].data)
    cb = plt.colorbar(cd, orientation = 'horizontal')
    plt.text(float(x1) - 1., float(y2) - 1., '(b)')
    plt.savefig(str(what_am_i)+'_10th_90th_percentile.png')
    plt.show()

 
if __name__ == "__main__":
    main(incube,outpath,what_am_i)            
