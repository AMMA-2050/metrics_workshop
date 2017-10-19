"""
This module contains utility functions for the metric atlas. These functions should not be changed by the user.
C. Klein 2017
"""

import os
import sys
import constants as cnst
import iris
import numpy as np
import glob
import pdb



def split_filename(filename):
    """
    Splits the file names of netCDF metric files and returns a dictionary for the different parts of the file name
    :param filename: string indicating the file name of any metric NetCDF file
    :return: dictionary
    """

    string = filename.split('_')

    if 'BC' in filename:

        file_dic = {'metric': string[0],
                    'variable': string[1],
                    'bc_res': string[2]+'_'+string[3],
                    'scenario': string[4],
                    'season' : string[5],
                    'region': string[6],
                    'filetype': string[7],
                    'aggregation' : string[8].split('.')[0]}

    else:

        file_dic = {'metric': string[0],
                    'variable': string[1],
                    'bc_res': string[2],
                    'scenario': string[3],
                    'season': string[4],
                    'region': string[5],
                    'filetype': string[6],
                    'aggregation': string[7].split('.')[0]}

    return file_dic


def split_filename_path(path):
    """
    Splits the file names of netCDF metric files and returns a dictionary for the different parts of the file name
    given the full path to that file
    :param path: full path to the netCDF file
    :return: dictionary
    """
    
    ano_file = os.path.basename(path)
    return split_filename(ano_file)



def order(file_list):
    """
    Sorts a given list of metric netCDF files to follow the order "historical, rcp26, rcp45, rcp85"
    :param file_list: list of metric netCDF files (full path or file names)
    :return: sorted list of same netCDF files
    """

    new_list = []

    for scen in cnst.SCENARIO:
        for f in file_list:

            if scen in f:
                new_list.append(f)

    return new_list


def load_data(file_path, xstart, xend, ystart, yend):
    """
    Opens a netCDF file and cuts out a box according to given coordinates
    :param file_path: string; full path to a netCDF file
    :param xstart: left x coordinate (longitude)
    :param xend: right x coordinate (longitude)
    :param ystart: bottom y coordinate (latitude)
    :param yend:  top y coordinate (latitude)
    :return: iris cube
    """

    mycube = iris.load(file_path)

    if len(mycube[0].shape) == 3:
        mycube = mycube[0]
    else:
        mycube = mycube[1]

    cubeout = mycube.intersection(latitude=(ystart, yend), longitude=(xstart, xend))

    return cubeout


def anomalies(hist, future, percentage=False):
    """
    Computes anomalies / percentage change from two Iris multi-model cubes (as returned from writeNetcdf.big_cube).
    Past and future anomaly ranges are defined in constants.py
    :param hist: multi-model iris cube for the historical time period
    :param future: multi-model iris cube for a future scenario
    :param percentage: boolean, whether the percentage change should be returned rather than absolute values
    :return: iris cube with anomaly
    """
    cubelist = iris.cube.CubeList([])
    mdls = hist.coord('model_name').points

    if hist.long_name != future.long_name:
        print 'Two different variables as input. Big big problem!'
        if (hist.long_name | future.long_name) == None:
            print 'Could be a minor problem, ignored'
            print hist.long_name
            print future.long_name
        else:
            pdb.set_trace()

    for mdl in mdls:

        mdlextract = iris.Constraint(model_name=lambda cell: cell == mdl)

        smll_future = future.extract(mdlextract)
        smll_past = hist.extract(mdlextract)

        try:
            differences = smll_future - smll_past  # if this fails a model is missing for a scenario
        except TypeError:
            continue
        except iris.exceptions.NotYetImplementedError:
            pdb.set_trace()

        if percentage:
            differences = 100 * ((smll_future - smll_past) / smll_past)

        cubelist.append(differences)

    anom = cubelist.merge_cube()

    return anom


def time_slicer(incube, scen):

    yearslicehist = iris.Constraint(year=lambda cell: cnst.HIST[0] <= cell <= cnst.HIST[1])
    yearslicefuture = iris.Constraint(year=lambda cell: cnst.FUTURE[0] <= cell <= cnst.FUTURE[1])

    if scen == 'historical':
        incube = incube.extract(yearslicehist)
    else:
        incube = incube.extract(yearslicefuture)

    return incube
