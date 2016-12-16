'''
load_data.py
This file will load the needed data to calculate our metrics
'''

import iris
import glob

def load_data(modelname,xstart,xend,ystart,yend):

    '''
    input
        modelname - the model name(including full filepath) that I wil bring in
        inpath - The path that the program should look for a file n>
        default: /nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/IPSL-CM5A-LR/historical/
        pr_WFDEI_1979-2013_0.5x0.5_day_IPSL-CM5A-LR_africa_historical_r1i1p1_full.nc
        cubeout -  The name of the cube to be returned to master
    return
        cubeout for further calculations
    '''
    
    cube = iris.load_cube(modelname)    
    cubeout = cube.intersection(latitude=(ystart,yend), longitude=(xstart, xend))       
    return cubeout

#if __name__ == "__main__": 
    #load_data(modelname,cubeout,xstart,xend,ystart,yend) 