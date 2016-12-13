'''
This script creates multi-model cubes and statistics, with model weighting 
'''
import iris
import numpy as np


def makeMMcube(model_names, ind, ipath):
    '''
    Make a multi-model cube for a given indicator
    Inputs
        - model_names : a list of model names that can be loaded into a multi-model cube
        - ind         : the name of an indicator that can be found in the filename
        - ipath       : the location to look for available files
    Output
        - ocube       : the multi-model cube
    Author: 
    '''
    import glob
    
    # Look for all files in a directory that contain the indicator name
    
    
    return(ocube)
    
def makeMultiModelStats(mm_cube, model_names, weights, ind, stat_name, opath):
    '''
    Apply model weights and create a statistic from the multi-model cube
    For example, we might want to return a multi-model MEAN of CWD, weighted more strongly towards 
    models that perform better for precipitation
    Inputs
        - mm_cube     : a multi-model cube containing a single indicator (iris 3D cube)
        - model_names : a list of model names (list of chr strings)
        - weights     : a list of weights that corresponds to model names (list of int)
        - ind         : the indicator name to look for
        - stat_name   : the statistic that we want to create (e.g. mean, std dev, percentiles, etc)
    Output
        - ocube       : a weighted cube that can be plotted
    Author: 
    '''
    
