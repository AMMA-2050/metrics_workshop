'''
load_data.py

this file will load the data needed to calculate our metrics
'''

import iris
import glob


def load_data(modelname, xstart, xend, ystart, yend):
    print 'This is the load data script'

    mycube = iris.load(modelname)
    if len(mycube[0].shape) == 3:
        mycube = mycube[0]
    else:
        mycube = mycube[1]
    print mycube.coord('longitude').points[0]
    print mycube.coord('longitude').points[-1]
    print mycube.coord('latitude').points[0]
    print mycube.coord('latitude').points[-1]
    cubeout = mycube.intersection(latitude=(ystart, yend), longitude=(xstart, xend))

    return cubeout

if __name__ == "__main__":
    load_data(modelname, xstart, xend, ystart, yend)
