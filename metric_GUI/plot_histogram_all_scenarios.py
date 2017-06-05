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

    #ok, so for this plot, we want to try and make a box and whiskers plot
    # of all the models for all 4 scenarios
    # so the first thing to do is check that all 4 scenarios exist
    histcube_name = file_searcher.replace(sc,'historical')
    rcp26_name = file_searcher.replace(sc,'rcp26')
    rcp45_name = file_searcher.replace(sc, 'rcp45')
    rcp85_name = file_searcher.replace(sc, 'rcp85')
    try:
       histcube = iris.load_cube(str(histcube_name)+'_all_models.nc')
       rcp26cube = iris.load_cube(str(rcp26_name)+'_all_models.nc')
       rcp45cube = iris.load_cube(str(rcp45_name)+'_all_models.nc')
       rcp85cube = iris.load_cube(str(rcp85_name)+'_all_models.nc')
    except IOError:
	print 'One or more files do not exist. Exiting Code'
    else: 


    # Ok, so the data that is coming in is 1D. So we just need to make a box and whiskers plot
    # The data we expect in is spatially averaged with one value per year.
    # So the first thing that we need to do is collapse by year

	    plt.clf()
	    histcube = histcube.collapsed('year',iris.analysis.MEDIAN)
	    rcp26cube = rcp26cube.collapsed('year', iris.analysis.MEDIAN)
	    rcp45cube = rcp45cube.collapsed('year', iris.analysis.MEDIAN)
	    rcp85cube = rcp85cube.collapsed('year', iris.analysis.MEDIAN)
            histmodels = np.ndarray.tolist(histcube.coord('model_name').points)
            rcp26models = np.ndarray.tolist(rcp26cube.coord('model_name').points)
            rcp45models = np.ndarray.tolist(rcp45cube.coord('model_name').points)
            rcp85models = np.ndarray.tolist(rcp85cube.coord('model_name').points)
	    # we also only want 1d data so need to collapse the data if it has longitude and latitude
            if len(histcube.coord('longitude').points) != 1:
                     histcube = histcube.collapsed('longitude', iris.analysis.MEAN)
            if len(histcube.coord('latitude').points) != 1:
                     histcube = histcube.collapsed('latitude', iris.analysis.MEAN)
            if len(rcp26cube.coord('longitude').points) != 1:
                     rcp26cube = rcp26cube.collapsed('longitude', iris.analysis.MEAN)
            if len(rcp26cube.coord('latitude').points) != 1:
                     rcp26cube = rcp26cube.collapsed('latitude', iris.analysis.MEAN)
            if len(rcp45cube.coord('longitude').points) != 1:
                     rcp45cube = rcp45cube.collapsed('longitude', iris.analysis.MEAN)
            if len(rcp45cube.coord('latitude').points) != 1:
                     rcp45cube = rcp45cube.collapsed('latitude', iris.analysis.MEAN)
            if len(rcp85cube.coord('longitude').points) != 1:
                     rcp85cube = rcp85cube.collapsed('longitude', iris.analysis.MEAN)
            if len(rcp85cube.coord('latitude').points) != 1:
                     rcp85cube = rcp85cube.collapsed('latitude', iris.analysis.MEAN)

	    hist = histcube.data
            rcp26 = rcp26cube.data
	    rcp45 = rcp45cube.data
            rcp85 = rcp85cube.data
            hist = np.ndarray.tolist(hist)
	    rcp26 = np.ndarray.tolist(rcp26)
	    rcp45 = np.ndarray.tolist(rcp45)
            rcp85 = np.ndarray.tolist(rcp85)
	    data = [hist,rcp26,rcp45,rcp85]
            histlist = np.arange(0.5, float(len(hist))+0.5, 1)
            rcp26list = np.arange(0.5, float(len(rcp26))+0.5, 1)
            rcp45list = np.arange(0.5, float(len(rcp45))+0.5, 1)
            rcp85list = np.arange(0.5, float(len(rcp85))+0.5, 1)

           # print histlist, hist
            labels = ['hist', 'rcp2.6','rcp4.5','rcp8.5']
            plt.subplot(2,2,1)
            plt.bar(histlist, hist)
            plt.xticks(histlist,histmodels, rotation = 'vertical')
            plt.title('historical') 
            plt.subplot(2,2,2)
            plt.bar(rcp26list, rcp26)
            plt.xticks(rcp26list,rcp26models, rotation = 'vertical')
            plt.title('RCP2.6')
            plt.subplot(2,2,3)
            plt.bar(rcp45list, rcp45)
            plt.xticks(rcp45list,rcp45models, rotation = 'vertical')
            plt.title('RCP4.5')
            plt.subplot(2,2,4)
            plt.bar(rcp85list, rcp85)
            plt.xticks(rcp85list,rcp85models, rotation = 'vertical')
            plt.title('RCP8.5')
            plt.tight_layout()
	    plt.savefig(str(what_am_i)+'_all_model_histogram.png')
	    plt.show()


 
if __name__ == "__main__":
    main(incube,outpath,what_am_i)            
