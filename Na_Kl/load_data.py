'''
load_data.py
this file will load the data needed to calculate our metrics
'''

import iris
import glob

def load_data(infile, ystart, yend, xstart, xend):
    '''
    inputs
        modelname -- the model name (including full filepath) that I will bring in
        coubeout -- the nma
    returns
        cubeout for further calculations    
    '''
    mycube = iris.load_cube(infile) 
    cubeout=mycube.intersection(latitude=(ystart, yend), longitude=(xstart, xend))

    return cubeout 

if __name__ == '__main__':
    
    load_data(modelname, inpath, ystart, yend, xstart, xend)