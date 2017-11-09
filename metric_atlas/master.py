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

def allScenarios_plot(inpath, outpath, bc_and_resolution, region, variable, season, metric):
    ###
    # Plots that need all scenarios at once
    ###



    for bc, var, seas in itertools.product(bc_and_resolution, variable, season):
        print 'All scenarios: ' + var
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



def singleScenario_plot(inpath, outpath, bc_and_resolution, region, variable, season, metric):
    ###
    # Plots that need a single scenario
    ###

    for bc, var, scen, seas in itertools.product(bc_and_resolution, variable, cnst.SCENARIO, season):
        print 'Single scenario: '+var

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


def saves():
    """
    Function to create all netcdf files that are needed for later plotting. All scenarios!
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

    atlas_utils.create_outdirs(outpath, bc_and_resolution)
    
    # Metric-specific options are set in constants.py
    for row in cnst.METRICS_TORUN:
        
        metric = row[0]
        variable = row[1]
        season = row[2]
        print '#######################################'
        print 'Saving data for: '
        print metric, variable, season
        print '#######################################'

        wNetcdf.run(variable, bc_and_resolution, inpath, outpath, season, metric, region, cnst.OVERWRITE)

    print 'All Netcdf files written, ready to plot!'


def wfdei_saves():
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

    # Metric-specific options are set in constants.py
    for row in cnst.METRICS_TORUN:
        metric = row[0]
        variable = row[1]
        season = row[2]
        print '#######################################'
        print 'Saving data for: '
        print metric, variable, season
        print '#######################################'

        wNetcdf.wfdei(variable, outpath, season, metric, region, cnst.OVERWRITE)

    print 'All Netcdf files written, ready to plot!'



def plot():

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
    for row in cnst.METRICS_TORUN:

        metric = row[0]
        variable = row[1]
        season = row[2]
        print '#######################################'
        print 'Plotting data for: '
        print metric, variable, season
        print '#######################################'

        allScenarios_plot(inpath, outpath, bc_and_resolution, region, variable, season, metric)
        singleScenario_plot(inpath, outpath, bc_and_resolution, region, variable, season, metric)

        print '#######################################'
        print 'Finished plotting'
        print '#######################################'

def main():
#    saves()
#    wfdei_saves()
#    plot()
    ca.runAtlas()


if __name__ == "__main__":
    main()
    