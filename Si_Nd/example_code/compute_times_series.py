'''
compute_times_series
'''
import os
import iris
import iris.coord_categorisation 


def compute_times_series(cube,ncfile):
    # Extract profiles of temperature and salinity from a particular point in
    # the southern portion of the domain, and limit the depth of the profile
    # to 1000m
    #lon_cons = iris.Constraint(longitude=330.5)
     #lat_cons = iris.Constraint(latitude=lambda l: -10 < l < -9)
     #cube.coord('latitude').guess_bounds()
     #cube.coord('latitude').guess_bounds()
     cubec = cube.collapsed(['longitude', 'latitude'], iris.analysis.MEAN)
     return(cubec)

     
    