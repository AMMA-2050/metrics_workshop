'''
make_big_cube
'''

import glob
import iris
import numpy as np
from iris.experimental.equalise_cubes import equalise_attributes
import os

def make_big_cube(file_searcher):
    
    list_of_files = glob.glob(file_searcher+'_single_model.nc')
    model_names = [f.split('/')[-1].split('_')[-1].split('.')[0] for f in list_of_files]

    cubelist = iris.cube.CubeList([])

    for file in list_of_files:
        
        fi = list_of_files.index(file)
        mod_coord = iris.coords.AuxCoord([model_names[fi]], long_name='model_name', var_name='model_name', units='1')

        cube = iris.load_cube(file)
        cube.data = np.ma.masked_invalid(cube.data)

        if fi == 0:
            template = cube.copy()
            cube.add_aux_coord(mod_coord, data_dims=None)
            cubelist.append(cube)
        else:
            newcube = template.copy()
            newcube.add_aux_coord(mod_coord, data_dims=None)
            newcube.data = cube.data
            cubelist.append(newcube)
    
    equalise_attributes(cubelist)
    bigcube = cubelist.merge_cube()

    iris.save(bigcube,str(file_searcher)+'_all_models.nc')
