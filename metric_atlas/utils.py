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

def read_metrics_avail(inpath):
    """
    Creates a list of available metrics given the path to the metric files folder
    :param inpath: string; path to the folder where all metric files are saved
    :return: a list with all available metrics based on which nc files were found
    """

    mlist = []
    ncfiles = glob.glob(inpath + os.sep + "*.nc")

    for nf in ncfiles:
        fname = os.path.basename(nf)
        mlist.append(fname.split('_')[0])
    metrics = np.array(mlist)
    print 'Available metrics from save files: '+ str(np.unique(metrics))
    return np.unique(metrics)


def create_outdirs(save_path, bc_and_resolution, metrics=None):
    """
    Creates the directory structure for saving netCDF metric files or plots created from these files. NetCDF metric files
    are saved in seperate folders depending on the chosen bias correction.
    Optionally, further sub-folders for every single metric can be created if these names are provided.
    :param save_path: string; path to folder in which 'save folder structure' should be created and metric nc files are saved
    :param bc_and_resolution: string list; the strings indicating bias correction and resolution
    :param metrics: string list of metric names, creates sub-folders for each single metric if provided
    :return: creates folder structure
    """

    for bc in bc_and_resolution:

        if bc not in cnst.BC_RES:
            print bc+' does not exist. Please check your resolution choice.'

        out = save_path + os.sep + bc

        if not os.path.isdir(out):
            try:
                os.makedirs(out)
            except OSError:
                sys.exit(bc + ' directory could not be created. Check path and permission')
        if metrics:
            inp = metrics + os.sep + bc
            mlist = read_metrics_avail(inp)
            for m in mlist:
                mpath = out + os.sep + m
                if not os.path.isdir(mpath):
                    try:
                        os.makedirs(mpath)
                    except OSError:
                        sys.exit(bc + ' directory could not be created. Check path and permission')


def split_imgname(filename):
    """
    Splits the file names of netCDF metric files and returns a dictionary for the different parts of the file name
    :param filename: string indicating the file name of any metric NetCDF file
    :return: dictionary
    """
    fileonly = os.path.basename(filename)
    string = fileonly.split('_')

    if 'BC' in filename:

        file_dic = {'metric': string[0],
                    'variable': string[1],
                    'bc_res': string[2]+'_'+string[3],
                    'season': string[4],
                    'region' : string[5],
                    'plotname': string[6],
                    'plottype': string[7].split('.')[0]
                    }

    else:

        file_dic = {'metric': string[0],
                    'variable': string[1],
                    'bc_res': string[2],
                    'season': string[3],
                    'region': string[4],
                    'plotname': string[5],
                    'plottype': string[6].split('.')[0]
                    }

    return file_dic


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

    for mdl in mdls:

        mdlextract = iris.Constraint(model_name=lambda cell: cell == mdl)

        smll_future = future.extract(mdlextract)
        smll_past = hist.extract(mdlextract)

        try:
            differences = smll_future - smll_past  # if this fails a model is missing for a scenario
        except TypeError:
            continue

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


def datalevels_ano(data):
    """
    Given a data array with positive and negative values, returns a list of 10 plotting levels with top and bottom
    corresponding to the 90th percentile value. Makes sure that diverging color bars are centred.
    :param data: anomaly data array
    :return: list of 10 data levels with same numbers for positive and negative values
    """
#    scalefacs = [1., 10., 100., 1000., 10000., 100000.]
    
    dmax = np.percentile(abs(data), 95)
    outlevels = np.linspace(-1 * int(dmax), int(dmax), 10)
    
#    for sf in scalefacs:
#        outlevels = np.linspace(-1 * int(dmax * sf)/sf, int(dmax * sf)/sf, 10)
#        if not np.all(outlevels == 0):
#            break
        
    
    if np.all(outlevels == 0):
        outlevels = np.round(np.linspace(-1 * int(dmax * 1000)/1000., int(dmax * 1000)/1000., 10), 2)
        
    return outlevels


def datalevels(data):
    """
    Given a data array with positive values, returns a list of 10 plotting levels with top and bottom corresponding to
    the 10th and 90th percentile values. Makes sure that color bar is not distorted by single high values determining
    the colorbar edges.
    :param data: data array with positive values only
    :return: list of 10 data levels
    """
    return np.linspace(int(np.percentile(data,10)), int(np.percentile(data, 90)), 10)


def data_minmax(datalist):
    """
    Returns symmetric positive and negative min/max axes limits for ordered data
    :param datalist: ordered data
    :return: absolute minimum and maximum of data
    """

    if np.abs(datalist[0]) < np.abs(datalist[-1]):
        vmin = np.abs(datalist[-1]) * -1
        vmax = np.abs(datalist[-1])
    else:
        vmin = np.abs(datalist[0]) * -1
        vmax = np.abs(datalist[0])

    return (vmin, vmax)