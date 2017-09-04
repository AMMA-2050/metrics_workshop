"""
Master script for writing netcdf files and plotting metrics
"""

import iris
import writeNetcdf as wNetcdf
import os
import mplot
import itertools
import constants as cnst
import utils
import pdb

iris.FUTURE.netcdf_promote = True

def allScenarios_plot(inpath, outpath, bc_and_resolution, region, variable, season, metric):
    ###
    # Plots that need all scenarios at once
    ###
    for bc, var, seas, reg in itertools.product(bc_and_resolution, variable, season, region):
        ### DOES NOT CHANGE
        cube_path = inpath + os.sep + bc + os.sep + str(metric) + '_' + str(var) + '_' + \
                    str(bc) + '_*_' + str(seas) + '_' + str(reg[0]) + '_allModels'
        out = outpath + os.sep + bc + os.sep + metric

        #### CHOICE OF PLOTS BELOW HERE
        mplot.boxplot_scenarios(cube_path, out, reg, anomaly=False)
        mplot.boxplot_scenarios(cube_path, out, reg, anomaly=True)
        mplot.lineplot_scenarios(cube_path, out, reg)
        mplot.barplot_scenarios(cube_path, out, reg, anomaly=False)
        mplot.barplot_scenarios(cube_path, out, reg, anomaly=True)
        mplot.nbModels_histogram_scenarios(cube_path, out, reg, anomaly=True)


def singleScenario_plot(inpath, outpath, bc_and_resolution, region, variable, season, metric):
    ###
    # Plots that need a single scenario
    ###
    for bc, var, scen, seas, reg in itertools.product(bc_and_resolution, variable, cnst.SCENARIO, season, region):

        if (scen == 'rcp26'):  # we leave rcp26 out for now - less plots!
            continue

        ### DOES NOT CHANGE
        cube_path = inpath + os.sep + bc + os.sep + str(metric) + '_' + str(var) + '_' + \
                    str(bc) + '_' + scen + '_' + str(seas) + '_' + str(reg[0]) + '_allModels'
        out = outpath + os.sep + bc + os.sep + metric
        #
        ### CHOICE OF PLOTS BELOW HERE
        # mplot.nbModels_histogram(cube_path, out, reg, anomaly=False)
        # mplot.nbModels_histogram(cube_path, out, reg, anomaly=True)

        mplot.modelRank_scatter_single(cube_path, out, reg, anomaly=False)
        mplot.modelRank_scatter_single(cube_path, out, reg, anomaly=True)

        mplot.map_percentile_single(cube_path, out, reg, anomaly=False)
        mplot.map_percentile_single(cube_path, out, reg, anomaly=True)


def saves():
    """
    Function to create all netcdf files that are needed for later plotting. All scenarios!
    :return: Netcdf files for single models (_singleModel.nc), multi-model cube (_allModels.nc) and anomalies per model
     in a multi-model cube in absolute values (_anomalies.nc) and in percentage change (_anomaliesPerc.nc).
    """

    ###
    # CHOOSE OPTIONS RELATED TO ALL METRICS
    ###
    #inpath = '/users/global/cornkle/CMIP/CMIP5_Africa'
    #outpath = '/users/global/cornkle/CMIP/CMIP5_Africa/save_files'
    inpath = cnst.DATADIR
    outpath = cnst.METRIC_DATADIR
    bc_and_resolution = cnst.BC_RES  # mdlgrid does not work cause models are not on the same grid!
    region = cnst.REGIONS_LIST #[cnst.REGIONS['WA'], cnst.REGIONS['BF']]

    utils.create_outdirs(outpath, bc_and_resolution)

    ###
    #Choose metric specific options
    ###
    variable = ['pr', 'tasmax']
    season = ['jas']
    calc_file = 'annualMax'
    overwrite = 'No'
    wNetcdf.run(variable, bc_and_resolution, inpath, outpath, season, calc_file, region, overwrite)

    ###
    #Choose metric specific options
    ###
    variable = ['tasmax']
    season = ['jas']
    calc_file = 'AnnualHotDaysPerc'
    overwrite = 'No'
    wNetcdf.run(variable, bc_and_resolution, inpath, outpath, season, calc_file, region, overwrite)

    ###
    # Choose metric specific options
    ###
    variable = ['tasmax']
    season = ['jas']
    calc_file = 'AnnualHotDays'
    overwrite = 'No'
    wNetcdf.run(variable, bc_and_resolution, inpath, outpath, season, calc_file, region, overwrite)

    ###
    # Choose metric specific options
    ###
    variable = ['pr']
    season = ['mjjas']
    calc_file = 'onsetMarteau'
    overwrite = 'No'
    wNetcdf.run(variable, bc_and_resolution, inpath, outpath, season, calc_file, region, overwrite)


    print('All Netcdf files written, ready to plot!')



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
    #inpath = '/users/global/cornkle/CMIP/CMIP5_Africa/save_files'
    #outpath = inpath + os.sep + 'plots'
    bc_and_resolution = cnst.BC_RES #['BC_0.5x0.5']
    region = cnst.REGIONS_LIST #[cnst.REGIONS['WA'], cnst.REGIONS['BF']]
    #####
    
    utils.create_outdirs(outpath, bc_and_resolution, metrics=inpath)

    ###
    #Start plot annual max metric
    ###
    variable = ['pr']
    season = ['jas']
    metric = 'annualMax'

    allScenarios_plot(inpath, outpath, bc_and_resolution, region, variable, season, metric)
    singleScenario_plot(inpath, outpath, bc_and_resolution, region, variable, season, metric)


    ###
    # Start plot nbTmax metric
    ###
    variable = ['tasmax']
    season = ['jas']
    metric = 'AnnualHotDays'

    allScenarios_plot(inpath, outpath, bc_and_resolution, region, variable, season, metric)
    singleScenario_plot(inpath, outpath, bc_and_resolution, region, variable, season, metric)


if __name__ == "__main__":
    saves()
    plot()
