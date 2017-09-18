"""
Contains global constants for the CMIP5 atlas
"""

DATADIR = '/Users/ajh235/Work/DataLocal/Projects/AMMA-2050' # '/project/FCFA/CMIP5/bias_corrected/WA_data'
METRIC_DATADIR = DATADIR + '/save_files/metric_data'
METRIC_PLOTDIR = DATADIR + '/save_files/metric_plots'
BC_RES = ['BC_0.5x0.5'] #['0.5x0.5', 'BC_0.5x0.5', 'BC_mdlgrid', 'mdlgrid']

SCENARIO = ['historical', 'rcp85'] #['historical', 'rcp26', 'rcp45', 'rcp85']

REGIONS = {'WA' : ['WA', 'West Africa', [-18, 25, 4, 25]],   # lon1, lon2, lat1, lat2
           'BF' : ['BF','Burkina Faso',[-6, 2.8, 9 ,15.5]],
           'SG' : ['SG', 'Senegal', [-18, -11, 12, 17]]
           }

REGIONS_LIST = [REGIONS['BF']] # [cnst.REGIONS['WA'], cnst.REGIONS['BF']]

AGGREGATION = ['tseries', '2d', 'trend']

FTYPES = ['singleModels', 'allModels', 'anomalies', 'anomaliesPerc']

VARNAMES = {'pr' : 'daily precipitation',
            'tas' : 'daily mean temperature',
            'tasmin' : 'daily minimum temperature',
            'tasmax' : 'daily maximum temperature'
            }

FUT_TREND = [2010, 2060]
FUTURE = [2040, 2069]
HIST = [1950, 2000]

HOTDAYS_THRESHOLD = 40

METRIC_AGGS = {
            'annualMax' : ['tseries', '2d', 'trend'],
            'annualMin' : ['tseries', '2d', 'trend'],
            'annualTotalRain' : ['tseries', '2d', 'trend'],
            'annualMean' : ['tseries', '2d', 'trend'],
            'monthlyClimatologicalMean' : ['tseries', '2d', 'trend'],
            'AnnualnbDayPerc' : ['tseries', '2d'],
            'AnnualHotDaysPerc' : ['tseries', '2d'],
            'AnnualRainyDaysPerc' : ['tseries', '2d'],
            'AnnualRainyDaysPerc50' : ['tseries', '2d'],
            'AnnualnbDay' : ['tseries', '2d', 'trend'],
            'AnnualHotDays' : ['tseries', '2d', 'trend'],
            'AnnualExtremeRain50' : ['tseries', '2d', 'trend'],
            'AnnualExtremeRain100' : ['tseries', '2d', 'trend'],
            'SPIxMonthly' : ['tseries', '2d'],
            'onsetMarteau' : ['tseries', '2d', 'trend'],
            'rainfallSequences10' : ['tseries', '2d'],
            'cdd' : ['tseries', '2d']
        }