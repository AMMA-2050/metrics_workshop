"""
Contains global constants for the CMIP5 atlas
"""

DATADIR = '/project/FCFA/CMIP5/bias_corrected/WA_data'
METRIC_DATADIR = DATADIR + '/save_files/metric_data'
METRIC_PLOTDIR = DATADIR + '/save_files/metric_plots'
BC_RES = ['BC_0.5x0.5'] #['0.5x0.5', 'BC_0.5x0.5', 'BC_mdlgrid', 'mdlgrid']

SCENARIO = ['historical', 'rcp85'] #['historical', 'rcp26', 'rcp45', 'rcp85']

REGIONS = {'WA' : ['WA', 'West Africa', [-18, 25, 4, 25]],   # lon1, lon2, lat1, lat2
           'BF' : ['BF','Burkina Faso',[-6, 2.8, 9 ,15.5]]}

REGIONS_LIST = [REGIONS['BF']] # [cnst.REGIONS['WA'], cnst.REGIONS['BF']]

AGGREGATION = ['tseries', '2d']

FTYPES = ['singleModels', 'allModels', 'anomalies', 'anomaliesPerc']

VARNAMES = {'pr' : 'daily precipitation',
            'tas' : 'daily mean temperature',
            'tasmax' : 'daily maximum temperature'}

FUTURE = [2040, 2069]
HIST = [1950, 2000]