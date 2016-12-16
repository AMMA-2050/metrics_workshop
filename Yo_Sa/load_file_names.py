'''
load_file_names
'''

import glob

def load_file_names(variable,scenario,bc_and_resolution):
    # /nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/IPSL-CM5A-LR/historical/tasmax_WFDEI_1979-2013_0.5x0.5_day_IPSL-CM5A-LR_africa_historical_r1i1p1_full.nc
     files_good = []
     filepath = '/nfs/a266/data/CMIP5_AFRICA/'+str(bc_and_resolution)+'/*/'+str(scenario)+'/'+str(variable)+'*.nc'
     files_good = glob.glob(filepath)
     modelID = [f.split('/')[-3] for f in files_good]
     print files_good[:]
     return([files_good, modelID])


if __name__ == "__main__":
    load_file_names(variable,scenario,bc_and_resolution)