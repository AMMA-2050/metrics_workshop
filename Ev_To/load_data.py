'''
this file will load the data needed to calculate our metrics

'''
import iris

def load_data(modelname,xstart,xend,ystart,yend):
    
    '''
inputs -
    modelname -the model name that I will bring in
    inpath - the path that the program should look for a file in.
    default: /nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/
    cubeout- The name of the cube to be retuned to master
    
returns -
    cubeout for further calculations.
    '''
    print 'this is the load data script'
    
    
    mycube = iris.load_cube(modelname)
    
    cubeout = mycube.intersection(latitude=(ystart, yend), longitude=(xstart,xend))
    
    return cubeout
    
    
if __name__ == "__main__":
    load_data()
    
      
    