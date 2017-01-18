'''
load_file_names
'''

import glob
import os

def load_file_names(inpath,variable,scenario,bc_and_resolution):
#    variable = 'pr'
#    bc_and_resolution = 'BC_0.5x0.5'
#    scenario = 'historical'
    files_good = []
    filepath = inpath+'/'+str(bc_and_resolution)+'/*/'+str(scenario)+'/'+str(variable)+'*.nc'
    print filepath
    files_good = glob.glob(filepath)
#    directory = '/nfs/a266/data/CMIP5_AFRICA/'+str(bc_and_resolution)+'/'
    modelID = [f.split(os.sep)[-3] for f in files_good]    
     
    return(files_good,modelID)            
    
    
if __name__ == "__main__":
    load_file_names(variable,scenario,bc_and_resolution)    
