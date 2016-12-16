'''
load_data.py

this file will load the data needed to calculate our metrics
Author: Siny NDOYE, December 2016
'''

import iris
import glob

def load_data(infile,xstart,xend,ystart,yend):
    '''
    Input - 
    modelname - the model name that I will bring in
    inpath - the path that the program should look for a file in.
    default : /nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/
    cubeout - The name of cube to be returned to master
    returns - 
    cubeout for further calculations.
    '''
    print 'This is the load data script'
        
    mycube = iris.load_cube(infile)
    cubeout = mycube.intersection(latitude=(ystart, yend), longitude=(xstart, xend))
    
    return(cubeout)
    
#    return cube out

    
     






if __name__ == "__main__":
    load_data()

