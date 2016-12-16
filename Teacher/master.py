'''
master.py
'''

import load_file_names
import load_data
import calc_hovmoller_precip
import make_big_cube
import make_big_plot
import iris

def master(variable,scenario,bc_and_resolution, outpath, season,region):
 #       files_good = []
    files_good, modelID = load_file_names.load_file_names(variable,scenario,bc_and_resolution)
#    print files_good[:]
    big_cube = iris.cube.CubeList([])
#    print modelID
    for fle in files_good:
    	   for nme in modelID:
    	       if nme in fle: nc_file = outpath+'/'+str(nme)+'_'+str(season)+'_'+str(region)+'.nc'
    	   try:
    	           cube2plot = iris.load(nc_file)
    	   except IOError:
    	       print nc_file                	           
               cubeout = load_data.load_data(fle,-10,10,-5,25)
               cube2plot = calc_hovmoller_precip.calc_hovmoller_precip(cubeout,'full_year',nc_file)
    bigcube = make_big_cube.make_big_cube(outpath)   
    make_big_plot.make_big_plot(bigcube)

if __name__ == "__main__":
    variable = 'pr'
    scenario = 'historical'
    bc_and_resolution = 'BC_0.5x0.5'
    outpath = '/nfs/a266/earv061/'
    season = 'whole_year'
    region = 'west_africa'
    master(variable,scenario,bc_and_resolution, outpath, season,region)
