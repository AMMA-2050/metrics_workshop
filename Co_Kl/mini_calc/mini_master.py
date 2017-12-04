import atlas_utils, calc, constants as cnst


#### We only need these seven strings to create clean output files.
# Please give the correct variable and scenario information, the rest is less important
metric = 'metricname'  # identifies the metric you're calculating
var = 'tas' # the CMIP5 variable name
bc = 'dummy' # we use this, you need to provide a random string (it's a bias correction flag)
sc = 'rcp45' #  scenario, could form a loop from cnst.SCENARIO
seas = 'jas' # season
reg = 'WestAfrica'  # regional flag
aggregation = cnst.AGGREGATION[0]


lonlatbox = [-18, 25, 4, 25]
cmip5_file = '/users/global/cornkle/CMIP/CMIP5_Africa/BC_mdlgrid/GFDL-CM3/rcp45/'+var+'_WFDEI_1979-2013_mdlgrid_day_GFDL-CM3_west-africa_rcp45_r1i1p1_full.nc'

outfilename = str(metric) + '_' +str(var) + '_' + str(bc) + \
                        '_' + str(sc) + '_' + str(seas) +'_' + str(reg) +'_singleModel_' + aggregation +'.nc'


outpath = '/users/global/cornkle/test/' + outfilename

cube = atlas_utils.load_data(cmip5_file, lonlatbox[0], lonlatbox[1],lonlatbox[2],lonlatbox[3])

calc.annualHotDays(cube, 'jas', outpath)

