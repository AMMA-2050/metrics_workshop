"""
Package to create all Netcdf files necessary for metric atlas plotting. Reads CMIP5 original data and writes
metric files for single models (*_single_model.nc), the big model cube (*_all_models.nc) and model anomalies in
a big cube between the historical and future periods (*_all_models_anomalies.nc), also given as percentage change 
(*_all_models_anomalies_perc.nc)
Anomalies are based on the median for the time period 1950-1999 (historical) and 2050-2099 (scenario).
Anomaly percentage change is with respect to the historical period. 

* Single models / big cube NetCDF files are saved as 3D cubes (lat,lon,time) without collapsing. 
* Anomalies are 2d cubes (lat,lon), collapsed over the years (median)


Input: strings defining the input netcdf files
Output: netcdf files for single models, big model cube and anomalies 
"""

import load_data
import make_big_cube
import iris
import itertools
import os
import glob
import pdb
import numpy as np

"""
Returns the path to CMIP5 files and model names
"""
def load_file_names(inpath, variable, scenario, bc_and_resolution):
    filepath = inpath + '/' + str(bc_and_resolution) + '/*/' + str(scenario) + '/' + str(variable) + '*.nc'
    print filepath
    files_good = glob.glob(filepath)

    modelID = [f.split(os.sep)[-3] for f in files_good]

    return (files_good, modelID)



"""
Computes respective metric and returns single model files and multi-model cube
"""
def model_files(variable, scenario, bc_and_resolution, inpath, outpath, season, calc_file, overwrite):
    ### generally use West Africa domain, plotting deals with sub-domains
    xmin = -18
    xmax = 25
    ymin = 4
    ymax = 25

    for sc, bc, seas, var in itertools.product(scenario, bc_and_resolution, season, variable):

        print inpath, sc, bc, seas
        files_good, modelID = load_file_names(inpath, var, sc, bc)

        if files_good == []:
            print 'No files found. Please check you chose an input directory!'
            return

        calc_file_load = 'calc_' + str(calc_file)
        calc_file_script = __import__(calc_file_load)

        for file, nme in zip(files_good, modelID):
            nc_file = outpath + '/' + str(calc_file) + '_' + str(bc) + '_' + str(sc) + '_' + str(
                seas) + '_' + str(nme) + '_single_model.nc'
            if os.path.isfile(nc_file) & (overwrite == 'No'):
                continue
            pdb.set_trace()
            cubeout = load_data.load_data(file, xmin, xmax, ymin, ymax)
            calc_file_script.main(cubeout, seas, nc_file)  # saves netcdf

        file_searcher = outpath + '/' + str(calc_file) + str(var) + '_' + str(bc) + '_' + str(sc) + '_' + str(seas)

        make_big_cube.make_big_cube(file_searcher)




"""
Computes and saves anomalies / percentage change from a multi-cube netcdf file for respective metrics
"""
def anomaly_files(variable, bc_and_resolution, path, season, calc_file, scenario):
    for sc, bc, seas, var in itertools.product(scenario, bc_and_resolution, season, variable):

        file_searcher = path + '/' + str(calc_file) + str(var) + '_' + str(bc) + '_' + sc + '_' + str(seas)
        sc_path = glob.glob(file_searcher + '_all_models.nc')
        hist_path = sc_big_cube.replace(str(sc), 'historical')

        hist_big_cube = iris.load_cube(hist_path)
        sc_big_cube = iris.load_cube(sc_path)

        yearslicehist = iris.Constraint(year=lambda cell: 1950 <= cell <= 1999)
        yearslicefuture = iris.Constraint(year=lambda cell: 2050 <= cell <= 2099)
        cubehist = hist_big_cube.extract(yearslicehist)
        cubefuture = sc_big_cube.extract(yearslicefuture)

        cubehist = cubehist.collapsed('year', iris.analysis.MEDIAN)
        cubefuture = cubefuture.collapsed('year', iris.analysis.MEDIAN)
        anom = cubefuture.copy()
        mdls = anom.coord('model_name').points
        mdls = np.ndarray.tolist(mdls)

        cubelist = []
        cubelist_perc = []
        for mdl in mdls:
            fi = mdls.index(mdl)
            mdlextract = iris.Constraint(model_name=lambda cell: cell == mdl)
            smllcubefuture = cubefuture.extract(mdlextract)
            smllcubepast = cubehist.extract(mdlextract)

            try:
                differences = smllcubefuture - smllcubepast
            except TypeError:
                continue

            differences_perc = 100 * ((smllcubefuture - smllcubepast) / smllcubepast)
            cubelist.append(differences)
            cubelist_perc.append(differences_perc)

        anom = cubelist.merge_cube()
        anom_percentage = cubelist_perc.merge_cube()

        iris.save(anom, file_searcher + '_all_models_anomalies.nc')
        iris.save(anom_percentage, file_searcher + '_all_models_anomalies_perc.nc')
