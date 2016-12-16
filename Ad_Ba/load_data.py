'''
load_data.py
this file will load the data needed to calculate our metrics
'''

import iris
import glob

def load_data(modelname,xstart,xend,ystart,yend):
    '''
    inputs:
        modelname: the model name that I will bring in
        inpath: the path that the program should look for a file in
        cubeout: the name of the cube to be returned to master
    returns: cubeout for futher calculations
    '''
    print "This is the load data script"
       
    cube = iris.load_cube(modelname)
    cubeout = cube.intersection(latitude=(ystart, yend), longitude=(xstart, xend))
    
    return cubeout

if __name__ == "__main__":
    load_data(modelname,xstart,xend,ystart,yend)
