import utils
import iris
import itertools
import os
import glob
import numpy as np

import sys
import pdb
from iris.experimental.equalise_cubes import equalise_attributes
from metric_atlas import writeNetcdf


out = '/users/global/cornkle/CMIP/CMIP5_Africa/allmodels/all_metric_data'
metric='annualMax'
var='tasmax'
bc = 'BC_0.5x0.5'
sc = 'historical'
seas = 'ann'
reg = 'BF'
agg = 'tseries'

file_searcher = out + os.sep + str(metric) + '_' +str(var) + '_' + str(bc) + \
                        '_' + str(sc) + '_' + str(seas) +'_' + str(reg)

writeNetcdf.big_cube(file_searcher, agg)