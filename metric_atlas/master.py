"""
Master script for writing netcdf files and plotting metrics
"""
# Needed by Andy to run internally on the Met Office system
import sys
#print sys.path
sys.path = [pth for pth in sys.path if '/usr/local/sci/lib' not in pth]
import iris
import writeNetcdf as wNetcdf
import os
import mplot
import itertools
import createAtlas as ca
import constants as cnst
import atlas_utils
import pdb
from multiprocessing import Pool

iris.FUTURE.netcdf_promote = True
iris.FUTURE.netcdf_no_unlimited = True


def allScenarios_plot(m):
    ###
    # Plots that need all scenarios at once
    ###
    inpath = m[0]
    outpath = m[1]
    bc_and_resolution = m[2]
    region = m[3]
    variable = m[4]
    season = m[5]
    metric = m[6]

    print '#######################################'
    print 'Plotting all scenarios for: '
    print metric, variable, season
    print '#######################################'


    for bc, var, seas in itertools.product(bc_and_resolution, variable, season):
        print 'All scenarios: ', var, seas
        ### DOES NOT CHANGE
        cube_path = inpath + os.sep + bc + os.sep + str(metric) + '_' + str(var) + '_' + \
                    str(bc) + '_*_' + str(seas) + '_' + str(region[0]) + '_allModels'
        out = outpath + os.sep + bc + os.sep + metric

        #### CHOICE OF PLOTS BELOW HERE

        if metric == 'monthlyClimatologicalMean':
            return

        mplot.boxplot_scenarios(cube_path, out, region, anomaly=True)

        #   mplot.barplot_scenarios(cube_path, out, reg, anomaly=True)
        #   mplot.boxplot_scenarios(cube_path, out, reg, anomaly=False)
        #   mplot.lineplot_scenarios(cube_path, out, reg)
        #   mplot.barplot_scenarios(cube_path, out, reg, anomaly=False)
        #   mplot.nbModels_histogram_scenarios(cube_path, out, reg, anomaly=False)
        #   mplot.nbModels_histogram_scenarios(cube_path, out, reg, anomaly=True)



def singleScenario_plot(m):
    ###
    # Plots that need a single scenario
    ###

    inpath = m[0]
    outpath = m[1]
    bc_and_resolution = m[2]
    region = m[3]
    variable = m[4]
    season = m[5]
    metric = m[6]

    print '#######################################'
    print 'Plotting single scenario for: '
    print metric, variable, season
    print '#######################################'

    for bc, var, scen, seas in itertools.product(bc_and_resolution, variable, cnst.SCENARIO, season):
        print 'Single scenario: ', var, scen, seas

        if (scen not in cnst.SINGLE_SCEN_PLOT):
            continue

        ### DOES NOT CHANGE
        cube_path = inpath + os.sep + bc + os.sep + str(metric) + '_' + str(var) + '_' + \
                    str(bc) + '_' + scen + '_' + str(seas) + '_' + str(region[0]) + '_allModels'
        out = outpath + os.sep + bc + os.sep + metric
        #
        ### CHOICE OF PLOTS BELOW HERE
        if metric == 'monthlyClimatologicalMean':
            mplot.boxplotMonthlyClim(cube_path, out, region, anomaly=True)
        else:
         #   mplot.nbModels_histogram_single(cube_path, out, reg, anomaly=False)
            mplot.nbModels_histogram_single(cube_path, out, region, anomaly=True)

         #   mplot.modelRank_scatter_single(cube_path, out, reg, anomaly=False)
            mplot.modelRank_scatter_single(cube_path, out, region, anomaly=True)

        #    mplot.map_percentile_single(cube_path, out, reg, anomaly=False)
            mplot.map_percentile_single(cube_path, out, region, anomaly=True)




def saves(multiprocessing=False):
    """
    Function to create all netcdf files that are needed for later plotting. All scenarios!

    Calls the functions to write single model, multi-model and anomaly NetCDF files.

    :param variable: string list of chosen variables: e.g. ['pr', 'tasmax']
    :param bc_and_resolution: string list of chosen correction option: e.g. ['BC_0.5x0.5' , '0.5x0.5']
    :param inpath: path to CMIP5 Africa directory: '/my/path/CMIP5_Africa'
    :param outpath: path where intermediate NetCDF files should be saved (single / multi-model / anomalies)
    :param season: string list months for which the metric is to be computed: ['jas', 'ann']
    :param metric: STRING identifing a metric (the calculation file), no list: 'annualMax'
    :param overwrite: whether or not existing NetCDF files should be overwritten

    :return: Netcdf files for single models (_singleModel.nc), multi-model cube (_allModels.nc) and anomalies per model
     in a multi-model cube in absolute values (_anomalies.nc) and in percentage change (_anomaliesPerc.nc).
    """

    ###
    # CHOOSE OPTIONS RELATED TO ALL METRICS
    ###
    inpath = cnst.DATADIR
    outpath = cnst.METRIC_DATADIR
    bc_and_resolution = cnst.BC_RES  # mdlgrid does not work cause models are not on the same grid!
    region = cnst.ATLAS_REGION
    scenarios = cnst.SCENARIO

    atlas_utils.create_outdirs(outpath, bc_and_resolution)
    multi_list = []
    for row in cnst.METRICS_TORUN:
        metric = row[0]
        variable = row[1]
        season = row[2]
        multi_list.append((variable, scenarios, bc_and_resolution, inpath, outpath, season, metric, region, cnst.OVERWRITE))
    
    print multi_list
    
    if multiprocessing:
        pool = Pool(processes=multiprocessing)
        res = pool.map(wNetcdf.model_files, multi_list)
        pool.close()
    else:
        # Metric-specific options are set in constants.py
        for m in multi_list:
            wNetcdf.model_files(m)

    print 'All Netcdf files written, ready to plot!'


def wfdei_saves(multiprocessing=False):
    """
    Function to create all netcdf files that are needed for later plotting. All scenarios!
    :return: Netcdf files for single models (_singleModel.nc), multi-model cube (_allModels.nc) and anomalies per model
     in a multi-model cube in absolute values (_anomalies.nc) and in percentage change (_anomaliesPerc.nc).
    """

    ###
    # CHOOSE OPTIONS RELATED TO ALL METRICS
    ###
    outpath = cnst.METRIC_DATADIR
    bc_and_resolution = ['WFDEI']  # mdlgrid does not work cause models are not on the same grid!
    region = cnst.ATLAS_REGION

    atlas_utils.create_outdirs(outpath, bc_and_resolution)
    multi_list = []
    for row in cnst.METRICS_TORUN:
        metric = row[0]
        variable = row[1]
        season = row[2]
        multi_list.append((variable, outpath, season, metric, region, cnst.OVERWRITE))

    print multi_list
    
    if multiprocessing:
        pool = Pool(processes=multiprocessing)
        res = pool.map(wNetcdf.wfdei, multi_list)
        #print res.get(timeout=1)
        pool.close()
    else:
    # Metric-specific options are set in constants.py
        for m in multi_list:
            wNetcdf.wfdei(m)

    print 'All Netcdf files written, ready to plot!'



def plot(multiprocessing=False):

    """
    Plotting script, could run loops. Has to define regions etc. (full cube is West Africa) 
    Plots must also handle collapsing e.g hovmoeller lon collapse if needed.
    """

    ###
    # USER CHOICE: SET OPTIONS RELATED TO ALL METRICS
    ###
    inpath = cnst.METRIC_DATADIR
    outpath = cnst.METRIC_PLOTDIR

    bc_and_resolution = cnst.BC_RES
    region = cnst.ATLAS_REGION
    #####
    
    atlas_utils.create_outdirs(outpath, bc_and_resolution, metrics=inpath)

    # Metric-specific options are set in constants.py

    multi_list = []
    for row in cnst.METRICS_TORUN:
        metric = row[0]
        variable = row[1]
        season = row[2]
        multi_list.append((inpath, outpath, bc_and_resolution, region, variable, season, metric))

    if multiprocessing:
        pool = Pool(processes=multiprocessing)
        res = pool.map(allScenarios_plot, multi_list)
        # print res.get(timeout=1)
        pool.close()
    else:
        # Metric-specific options are set in constants.py
        for m in multi_list:
            allScenarios_plot(m)

    if multiprocessing:
        pool = Pool(processes=multiprocessing)
        res = pool.map(singleScenario_plot, multi_list)
        # print res.get(timeout=1)
        pool.close()
    else:
        # Metric-specific options are set in constants.py
        for m in multi_list:
            singleScenario_plot(m)

    print '#######################################'
    print 'Finished plotting'
    print '#######################################'



def main():

    for reg in cnst.REGIONS:

        #saves(multiprocessing=16) # multiprocessing=16
        #wfdei_saves(multiprocessing=16) # multiprocessing=16
        #plot()
        cnst.ATLAS_REGION = reg
        for m in cnst.AGG_PERIODS:
            ca.runAtlas(m)


def atlas():
    #for m in cnst.AGG_PERIODS:
    m = cnst.AGG_PERIODS[0]
    ca.runAtlas(m)


if __name__ == "__main__":
    main()
    
