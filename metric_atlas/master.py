"""
Master script for writing netcdf files and plotting metrics
"""

import writeNetcdf as wNetcdf
import plot_10th_percentile_all_models as perc10

def saves():

    inpath = 'C://Users/cornkle/OneDrive - NERC/data/CMIP5_Africa/'
    outpath = 'C://Users/cornkle/OneDrive - NERC/data/CMIP5_Africa/save_files'

    bc_and_resolution = ['WA_0.5x0.5']
    variable = 'pr'
    scenario = ['historical']
    season = ['jas']
    calc_file = 'annual_max'
    overwrite = 'No'

    # write all single model and big_cube files - make sure all scenarios are written for anomaly files!
    wNetcdf.model_files(variable, scenario, bc_and_resolution, inpath, outpath, season, calc_file, overwrite)
    wNetcdf.anomaly_files(variable, bc_and_resolution, outpath, season, calc_file, scenario)

    print('All Netcdf files written, ready to plot!')


def plot():

    """
    Plotting script, could run loops. Has to define regions etc. (full cube is West Africa) 
    Plots must handle collapsing e.g hovmoeller lon collapse if needed. 
    
    :return: 
    """

    saves_path = 'C://Users/cornkle/OneDrive - NERC/data/CMIP5_Africa/save_files'

    bc_and_resolution = ['WA_0.5x0.5']
    variable = 'pr'
    scenario = ['historical']
    season = ['jas']
    calc_file = 'annual_max'
    overwrite = 'No'
    region = [-10,10,5,9]

    cube_path = saves_path+'/'+ str(calc_file) + str(variable) + '_' + \
                str(bc_and_resolution) + '_' + str(scenario) + '_' + str(season) + '_all_models_anomalies.nc'

    perc10.main(cube_path, region=region)



