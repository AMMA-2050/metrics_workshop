'''
load_file_names.py

'''

import glob

def load_file_names(variable,scenario,bc_and_resolution):
    # This is an example of wha
    # variable = 'pr'
    # bc_and_resolution = 'BC'
    # scenario = historical
    files_good=[]
    filepath='/nfs/a266/data/CMIP5_AFRICA/'+str(bc_and_resolution)+'/*/'+str(scenario)+'/'+str(variable)+'*.nc'
    print filepath
    files_good = glob.glob(filepath)
    modelID = [f.split('/')[-3] for f in files_good]
    print files_good[:]
    return([files_good, modelID])

if __name__ == '__main__':
    
    load_file_names(variable,scenario,bc_and_resolution)