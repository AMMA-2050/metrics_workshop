import master


variable = 'pr'
scenario = ['rcp45']
bc_and_resolution = ['WA_data']
inpath = 'D://CMIP5/CMIP5_Africa'
outpath ='D://CMIP5/save_files'
season = ['jas']
region = 'West_Africa'
calc_file = 'mean_rain'
xmin = -10
xmax = 10
ymin = 5
ymax = 25
plotter = 'plot_histogram_anomaly'
overwrite = 'No'


master.master(variable, scenario, bc_and_resolution, inpath, outpath, season, region, calc_file, xmin, xmax, ymin, ymax,
           plotter, overwrite)



