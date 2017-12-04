import utils
import iris
import itertools
import os
import glob
import numpy as np
from metric_atlas import constants as cnst
import sys
import pdb
from iris.experimental.equalise_cubes import equalise_attributes
from metric_atlas import writeNetcdf
from metric_atlas import utils

def model_files(variable, scenario, bc_and_resolution, inpath, outpath, season, metric, region, overwrite):
    """
    Computes respective metric and returns single model files and multi-model cube at different aggregations
    """

    for sc, bc, seas, var, reg in itertools.product(scenario, bc_and_resolution, season, variable, region):

        out = outpath

        file_searcher = out + os.sep + str(metric) + '_' + str(var) + '_' + str(bc) + \
                        '_' + str(sc) + '_' + str(seas) + '_' + str(reg[0])

        for agg in cnst.METRIC_AGGS[metric]:
            #            pdb.set_trace()
            writeNetcdf.big_cube(file_searcher, agg)


inpath = cnst.DATADIR
outpath = '/users/global/cornkle/CMIP/CMIP5_Africa/allmodels/all_metric_data'
bc_and_resolution = cnst.BC_RES  # mdlgrid does not work cause models are not on the same grid!
region = cnst.REGIONS_LIST

utils.create_outdirs(outpath, bc_and_resolution)

# Metric-specific options are set in constants.py
for row in cnst.METRICS_TORUN:
    metric = row[0]
    variable = row[1]
    season = row[2]
    print '#######################################'
    print 'Saving data for: '
    print metric, variable, season
    print '#######################################'


    model_files(variable, cnst.SCENARIO, bc_and_resolution, inpath, outpath, season, metric, region, cnst.OVERWRITE)

print 'All Netcdf files written, ready to plot!'


