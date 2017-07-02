import iris
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as bm
import numpy as np
import os

def main(cube_path, region=None):

    incube = iris.load_cube(cube_path)
    file = os.path.basename(incube)
    name = incube[0:-3]

    if region:
        incube = incube.intersection(latitude=(region[0], region[1]), longitude=(region[2], region[3]))

    # find boundaries for map
    x1 = incube.coord('longitude').points[0]
    x2 = incube.coord('longitude').points[-1]
    y1 = incube.coord('latitude').points[0]
    y2 = incube.coord('latitude').points[-1]
    lon = incube.coord('longitude').points
    lat = incube.coord('latitude').points

    percentiles = incube.collapsed('model_name', iris.analysis.PERCENTILE, percent=[ 10,90])

    parspace = 5
    medspace = 5

    f = plt.figure()
    f.add_subplot(2,1,1)
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
    cb.set_label('10th Percentile ensemble anomaly')
    plt.text(float(x1) - 1., float(y2) - 1., '(a)')
    plt.subplot(2,1,2)
    m = bm.Basemap(projection='cyl',llcrnrlat = y1, urcrnrlat = y2, llcrnrlon = x1, urcrnrlon = x2,  resolution = 'h')
    m.drawcoastlines(linewidth= 2)
    m.drawcountries(linewidth = 1)     
    if medspace >= 1.0:    
         meridians = np.arange(x1, x2, float(medspace))
         m.drawmeridians(meridians, labels = [False, False, False, True])
    if parspace >= 1.0:
         parallels = np.arange(y1,y2,float(parspace))  
         m.drawparallels(parallels, labels = [False,True,False,False])

    cd = plt.contourf(lon,lat,percentiles[1,:,:].data)
    cb = plt.colorbar(cd, orientation = 'horizontal')
    cb.set_label('90th Percentile ensemble anomaly')
    plt.text(float(x1) - 1., float(y2) - 1., '(b)')
    plt.savefig(str(name)+'_10th_90th_percentile.png')
    plt.show()

 
if __name__ == "__main__":
    main(incube,outpath,what_am_i)            
