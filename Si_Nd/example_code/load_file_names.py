'''
load_file_names
'''

import glob
import os

def load_file_names(variable,scenario,bc_and_resolution):
#   variable = 'pr'
#   bc_and_resolution= 'BC_0.5*0.5'
#   scenario = 'historical'
    files_good=[]
    filepath = '/nfs/a266/data/CMIP5_AFRICA/' + str(bc_and_resolution) + '/*/' + str(scenario) + '/' + str(variable) + '*.nc'
    files_good=glob.glob(filepath)
    #print files_good[:]
    modelID = [f.split('/')[-3] for f in files_good]

    return (files_good,modelID)
   
    
#if __name__ == "__main__":
#    load_file_names()
