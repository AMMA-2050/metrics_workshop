'''
This is the master script that controls the processing chain
'''
import iris
import numpy as np
# Import local scripts
import loadData as ld
import calcMetrics as cm
import plotData as pdata
import multiModelStats as mms
import multiModelPlots as mmp

# To ensure that netcdfs are loaded correctly 
iris.FUTURE.netcdf_promote = True

def getIndexLongName(shortname):
    
    '''
    A function to retrieve the long name of the indicator for plotting etc.
    Inputs  : shortname is a standard abbreviation of the indicator as a character string
    Outputs : the long name of the indicator as a character string
    Author: Andy Hartley, 12/12/2016
    '''
    indicator_dict = {'CDD' : 'Consecutive Dry Days',
                      'CWD' : 'Consecutive Wet Days'
    }
    try:
        return(indicator_dict[shortname])
    except:
        return('Indicator '+shortname+' doesn\'t exist in the dictionary')


def getRegionCoords(regname):
    '''
    Returns the coordinates of the specified region as a list in the following order:
    [xmin, ymin, xmax, ymax]
    Inputs  : regname is a standard region name as a character string
    Outputs : 
    Author: Andy Hartley, 12/12/2016
    '''
    
    region_dict = {'west_africa': [-20.0, 0.0, 30.0, 30.0],
                   'senegal'    : [1.0, 2.0, 3.0, 4.0],
                   'burkina'    : [1.0, 2.0, 3.0, 4.0],
                   'sahel'    : [1.0, 2.0, 3.0, 4.0]
    }
    
    try:
        return(indicator_dict[shortname])
    except:
        return('Indicator '+shortname+' doesn\'t exist in the dictionary')


def main():
    
    ipath          = "/Users/ajh235/Work/Projects/AMMA-2050/"
    opath          = "/Users/ajh235/Work/Projects/AMMA-2050/Indicators/"
    figdir         = "/Users/ajh235/Work/Projects/AMMA-2050/Plots/"
    datatypes      = ["0.5x0.5", "BC_0.5x0.5", "BC_mdlgrid", "mdlgrid", "WFDEI"]
    indicator_list = ['CDD', 'CWD']
    # Might be enough to run indicators for the full region, but we could imagine 
    # timeseries plots for smaller regions such as 'sahel', 'senegal', 'burkina'
    region_names   = ['west_africa']
    season_names   = ['June', 'July', 'August', 'September', 'October', 'JAS', 'JJ', 'JA', 'AS', 'SO']
    model_names    = ['ACCESS1-0', 'ACCESS1-3', 'bcc-csm1-1', 'bcc-csm1-1-m', 'BNU-ESM', 'CanESM2', 'CMCC-CESM', 'CMCC-CM', 'CMCC-CMS', 'CNRM-CM5', 'CSIRO-Mk3-6-0', 'GFDL-CM3', 'GFDL-ESM2G', 'GFDL-ESM2M', 'HadGEM2-AO', 'HadGEM2-CC', 'HadGEM2-ES', 'inmcm4', 'IPSL-CM5A-LR', 'IPSL-CM5A-MR', 'IPSL-CM5B-LR', 'MIROC-ESM', 'MIROC-ESM-CHEM', 'MIROC5', 'MIROCC5', 'MPI-ESM-LR', 'MPI-ESM-MR', 'MRI-CGCM3', 'MRI-ESM1', 'NorESM1-M']
    
    #for regname in region_names:
    #    for seas in season_names:
            for dtyp in datatypes:
                #for ind in indicator_list:
                    for modname in modnames:

                        # Load the data we need
                        cube = ld.loadDaily(inpath, modname, 'West_Africa', rcp, dtyp)
                        
                        # Call metrics script, which does:
                        #   - load data
                        #   - 
                        if 'CDD' in indicator_list:
                            call_CDD_code(model_names, seasons_list, regions_list, outdir, figdir, overwrite=overwrite)
                            doPlotting()
                        
                        # Calculate the current indicator (untested)
                        #methodToCall = getattr(ci, ind) # Looks for the name of the indicator in the list of functions in this module
                        #cube_cdd = methodToCall(incube, opath, modname, regname, dtyp) # Calls the function
                        
                        
                        # Plot the individual model
                        pdata.plotModel(mod_cube, figdir)
                    
                    # After we've done everything for each model, now create multi-model stats and plots
                    mm_cube = mms.makeMMcube(modnames)
                    mmp.plotWeightedMaps(wmm_cube, figdir)
                    
    

if __name__ == '__main__':
    main()
