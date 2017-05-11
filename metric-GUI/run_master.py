import master


variable = 'pr'
scenario = ['rcp45']
bc_and_resolution = ['WA_data']
inpath = 'D://CMIP5/CMIP5_Africa'
outpath ='D://CMIP5/save_files'
season = ['mjjas']
region = ['West_Africa']
calc_file = 'Marteau_onset'
xmin = -10
xmax = 10
ymin = 5
ymax = 25
plotter = 'contourf_map'
overwrite = 'No'


master.master(variable, scenario, bc_and_resolution, inpath, outpath, season, region, calc_file, xmin, xmax, ymin, ymax,
           plotter, overwrite)



