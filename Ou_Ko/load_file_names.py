'''
load_file_names
'''

import glob

def load_file_names(variable,scenario,bc_and_resolution):
    
    #file_good =[]
    filepath = '/nfs/a266/data/CMIP5_AFRICA/'+str(bc_and_resolution)+'/*/'+str(scenario)+'/'+str(variable)+'*.nc'
    file_good = glob.glob(filepath)
    modelID = [f.split('/')[-3] for f in file_good]
    #print file_good[:]
    return([file_good, modelID])
    
#if __name__ == "__main__": 
    #load_file_names(variable,scenario,bc_and_resolution)