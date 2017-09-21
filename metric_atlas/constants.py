"""
Contains global constants for the CMIP5 atlas
"""

DATADIR = '/project/FCFA/CMIP5/bias_corrected/WA_data' #'/users/global/cornkle/CMIP/CMIP5_Africa' #'/Users/ajh235/Work/DataLocal/Projects/AMMA-2050' #'/project/FCFA/CMIP5/bias_corrected/WA_data'
METRIC_DATADIR = DATADIR + '/save_files/metric_data'
METRIC_PLOTDIR = DATADIR + '/save_files/metric_plots'
METRIC_ATLASDIR = DATADIR + '/save_files/metric_atlas'
BC_RES = ['BC_0.5x0.5'] #['0.5x0.5', 'BC_0.5x0.5', 'BC_mdlgrid', 'mdlgrid']

SCENARIO = ['historical', 'rcp85'] #['historical', 'rcp26', 'rcp45', 'rcp85']

REGIONS = {'WA' : ['WA', 'West Africa', [-18, 25, 4, 25]],   # lon1, lon2, lat1, lat2
           'BF' : ['BF','Burkina Faso',[-6, 2.8, 9 ,15.5]],
           'SG' : ['SG', 'Senegal', [-18, -11, 12, 17]]
           }

REGIONS_LIST = [REGIONS['BF']]

AGGREGATION = ['tseries', '2d', 'trend']

FTYPES = ['singleModels', 'allModels', 'anomalies', 'anomaliesPerc']

VARNAMES = {'pr' : 'daily precipitation',
            'tas' : 'daily mean temperature',
            'tasmin' : 'daily minimum temperature',
            'tasmax' : 'daily maximum temperature',
            'rsds' : 'surface downwelling shortwave radiation',
            'wind' : 'near surface wind speed'
            }

FUT_TREND = [2010, 2060]
FUTURE = [2040, 2069]
HIST = [1950, 2000]

HOTDAYS_THRESHOLD = 40
RAINYDAY_THRESHOLD = 1
STRONGWIND_THRESHOLD = 70

METRIC_AGGS = {
            'annualMax' : ['tseries', '2d', 'trend'],
            'annualMin' : ['tseries', '2d', 'trend'],
            'annualTotalRain' : ['tseries', '2d', 'trend'],
            'annualMean' : ['tseries', '2d', 'trend'],
            'annualMeanRainyDay' : ['tseries', '2d', 'trend'],
            'monthlyClimatologicalMean' : ['tseries', '2d', 'trend'],
            'annualHotDaysPerc' : ['tseries', '2d'],
            'annualRainyDays' : ['tseries', '2d'],
            'annualRainyDaysPerc' : ['tseries', '2d'],
            'annualHotDays' : ['tseries', '2d', 'trend'],
            'annualExtremeRain30' : ['tseries', '2d', 'trend'],
            'annualExtremeRain50' : ['tseries', '2d', 'trend'],
            'annualExtremeRain100' : ['tseries', '2d', 'trend'],
            'annualStrongWindDays' : ['tseries', '2d', 'trend'],
            'wetSpell10': ['tseries', '2d'],
            'drySpell6': ['tseries', '2d'],
            'annualMaxRain_5dSum': ['tseries', '2d'],
            'annualMaxRain_3dSum' : ['tseries', '2d'],
            'annualMaxRain_2dSum' : ['tseries', '2d'],
            'annualMaxRain_5dMean': ['tseries', '2d'],
            'annualMaxRain_3dMean': ['tseries', '2d'],
            'annualMaxRain_2dMean': ['tseries', '2d'],
            'SPIxMonthly' : ['tseries', '2d'],
            'onsetMarteau' : ['tseries', '2d', 'trend'],
            'cdd' : ['tseries', '2d']
        }


OVERWRITE = 'No' # 'Yes'

#######################################
# Choose metric specific options
#######################################
# metric, variable, season
# metric: exact name as appears in calc.py as a character string
# variable: list of climate variable(s) to send to the calc function
# season: list of seasons to run the metric-variable combination for
METRICS_TORUN = [
            ['annualMax', ['pr','tasmax', 'rsds'], ['jas']],
            ['annualMin', ['tasmin'], ['jas']],
            ['annualTotalRain', ['pr'], ['jas']],
            ['annualMean', ['tas', 'rsds'], ['jas']],
            ['annualMeanRainyDay', ['pr'], ['jas']],
            ['monthlyClimatologicalMean', ['pr', 'tasmin', 'tas', 'tasmax', 'rsds', 'wind'], ['jas']],
            #['annualHotDaysPerc', ['tasmax'], ['jas']],
            ['annualRainyDays', ['pr'], ['jas']],
            #['annualRainyDaysPerc', ['pr'], ['jas']],
            ['annualHotDays', ['tasmax'], ['jas']],
            ['annualExtremeRain30', ['pr'], ['jas']],
            ['annualExtremeRain50', ['pr'], ['jas']],
            ['annualExtremeRain100', ['pr'], ['jas']],
            ['annualStrongWindDays', ['wind'], ['jas']],
            ['wetSpell10', ['pr'], ['jas']],
            ['drySpell6', ['pr'], ['jas']],
            ['annualMaxRain_5dSum', ['pr'], ['jas']],
            ['annualMaxRain_3dSum', ['pr'], ['jas']],
            ['annualMaxRain_2dSum', ['pr'], ['jas']],
            ['annualMaxRain_5dMean', ['pr'], ['jas']],
            ['annualMaxRain_3dMean', ['pr'], ['jas']],
            ['annualMaxRain_2dMean', ['pr'], ['jas']],
            ['SPIxMonthly', ['pr'], ['jas']],
            ['onsetMarteau', ['pr'], ['mjjas']]
    ]

