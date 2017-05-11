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
    if len(percentiles.coord('time').points) > 1:
        percentiles = percentiles.collapsed('time', iris.analysis.SUM)
#    iris.coord_categorisation.add_year(percentiles, 'time', name = 'year')
#    averages = percentiles.collapsed('year', iris.analysis.MEDIAN)
    print percentiles
    plt.clf()
    cbvar = raw_input("Please type what variable is shown in color bar (e.g. Onset date for calc_Marteau)")
    parspace = 5
    medspace = 5
    medspace = raw_input("Please type how many degrees you want between longitude markings (default = 5)")
    parspace = raw_input("Please type how many degrees you want between latitude markings (default = 5)")
    plt.subplot(2,1,1)
    m = bm.Basemap(projection='cyl',llcrnrlat = y1, urcrnrlat = y2, llcrnrlon = x1, urcrnrlon = x2,  resolution = 'h')
    m.drawcoastlines(linewidth= 2)
    m.drawcountries(linewidth = 1)
    if medspace >= 1.0:    
         meridians = np.arange(x1, x2, float(medspace))
         m.drawmeridians(meridians, labels = [False, False, False, True])
    if parspace >= 1.0:
         parallels = np.arange(y1,y2,float(parspace))  
         m.drawparallels(parallels, labels = [False,True,False,False])

    cd = plt.contourf(lon,lat,percentiles[0,:,:].data)
    cb = plt.colorbar(cd, orientation = 'horizontal')
    cb.label('10th Percentile '+str(cbvar)+' ensemble anomaly')
    plt.text(float(x1) - 1., float(y2) - 1., '(a)')
    plt.subplot(2,1,2)
    m = bm.Basemap(projection='cyl',llcrnrlat = y1, urcrnrlat = y2, llcrnrlon = x1, urcrnrlon = x2,  resolution = 'h')
    m.drawcoastlines(linewidth= 2)
    m.drawcountries(linewidth = 1)     
    if medspace >= 1.0:    
         meridians = np.arange(x1, x2, medspace)
         m.drawmeridians(meridians, labels = [False, False, False, True])
    if parspace >= 1.0:
         parallels = np.arange(y1,y2,parspace)  
         m.drawparallels(parallels, labels = [False,True,False,False])

    cd = plt.contourf(lon,lat,percentiles[1,:,:].data)
    cb = plt.colorbar(cd, orientation = 'horizontal')
    cb.label('90th Percentile '+str(cbvar)+' ensemble anomaly')
    plt.text(float(x1) - 1., float(y2) - 1., '(b)')
    plt.savefig(str(what_am_i)+'_10th_90th_percentile.png')
    plt.show()

 
if __name__ == "__main__":
    main(incube,outpath,what_am_i)            
