"""
Contains global constants for the CMIP5 atlas
"""
VERSION = 'v0.2.2'
DATADIR = '/users/global/cornkle/CMIP/CMIP5_Africa' #'/users/global/cornkle/CMIP/CMIP5_Africa' #'/Users/ajh235/Work/DataLocal/Projects/AMMA-2050' #'/project/FCFA/CMIP5/bias_corrected/WA_data'
REGIONS = {'WA' : ['WA', 'West Africa', [-18, 25, 4, 25], 'WA_files'],   # lon1, lon2, lat1, lat2
           'BF' : ['BF','Burkina Faso',[-6, 2.8, 9 ,15.5], 'Burkina_files'],
           'SG' : ['SG', 'Senegal', [-18, -11, 12, 17], 'Senegal_files']
           }
#### whole process chain for one region at a time
ATLAS_REGION = REGIONS['BF']

METRIC_DATADIR = DATADIR + '/metric_atlas/' + ATLAS_REGION[3] +'/save_files/netcdf'
METRIC_PLOTDIR = DATADIR + '/metric_atlas/' + ATLAS_REGION[3] + '/save_files/plots'
METRIC_ATLASDIR = DATADIR + '/metric_atlas/' + ATLAS_REGION[3]
BC_RES = ['BC_0.5x0.5'] #['0.5x0.5', 'BC_0.5x0.5', 'BC_mdlgrid', 'mdlgrid']

SCENARIO = ['historical', 'rcp26', 'rcp45', 'rcp85'] #['historical', 'rcp85'] # ['historical', 'rcp85'] #

AGGREGATION = ['tseries', '2d', 'trend']

FTYPES = ['singleModels', 'allModels', 'anomalies', 'anomaliesPerc']

VARNAMES = {'pr' : 'daily precipitation',
            'tas' : 'daily mean temperature',
            'tasmin' : 'daily minimum temperature',
            'tasmax' : 'daily maximum temperature',
            'rsds' : 'surface downwelling shortwave radiation',
            'wind' : 'near surface wind speed',
            'multivars' : 'multiple input variables'
            }

FUT_TREND = [2010, 2060]
FUTURE = [2040, 2059]
HIST = [1950, 2000]

HOTDAYS_THRESHOLD = 40
RAINYDAY_THRESHOLD = 1
STRONGWIND_THRESHOLD = 30 # Values in 1 sample file have a historical max of 7 to 9, so this value is still far too high

METRIC_AGGS = {
            'annualMax' : ['tseries', '2d', 'trend'],
            'annualMin' : ['tseries', '2d', 'trend'],
            'annualTotalRain' : ['tseries', '2d', 'trend'],
            'annualMean' : ['tseries', '2d', 'trend'],
            'annualMeanRainyDay' : ['tseries', '2d', 'trend'],
            'monthlyClimatologicalMean' : ['tseries'], # Removed '2d', 'trend' because they don't really make sense
            'annualHotDaysPerc' : ['tseries', '2d', 'trend'],
            'annualRainyDays' : ['tseries', '2d', 'trend'],
            'annualRainyDaysPerc' : ['tseries', '2d'],
            'annualHotDays' : ['tseries', '2d', 'trend'],
            'annualExtremeRain30' : ['tseries', '2d', 'trend'],
            'annualExtremeRain50' : ['tseries', '2d', 'trend'],
            'annualExtremeRain100' : ['tseries', '2d', 'trend'],
            'annualStrongWindDays' : ['tseries', '2d', 'trend'],
            'wetSpell10': ['tseries', '2d'],
            'drySpell6': ['tseries', '2d'],
            'annualMaxRain5dSum': ['tseries', '2d'],
            'annualMaxRain3dSum' : ['tseries', '2d'],
            'annualMaxRain2dSum' : ['tseries', '2d'],
            'annualMaxRain5dMean': ['tseries', '2d'],
            'annualMaxRain3dMean': ['tseries', '2d'],
            'annualMaxRain2dMean': ['tseries', '2d'],
            'SPIxMonthly' : ['tseries', '2d'],
            'SPIbiannual' : ['tseries', '2d'],
            'onsetMarteau' : ['tseries', '2d', 'trend'],
            'pet' : ['tseries', '2d', 'trend']
        }

OVERWRITE = 'No' # 'Yes'

#######################################
# Choose metric specific options
#######################################
# metric, variable, season
# metric: exact name as appears in calc.py as a character string
# variable: list of climate variable(s) to send to the calc function
# season: list of seasons to run the metric-variable combination for

## monthlyClimatologicalMean and onsetMarteau are exceptions to the atlas aggregation period!
## Their aggregation period never changes.

AGG_PERIODS = ['jas']
METRICS_TORUN = [
    # ['annualMax', ['pr'], AGG_PERIODS],  # , # ,  'tasmax', 'rsds'
    # ['annualMin', ['tasmin'], AGG_PERIODS],
    # ['annualTotalRain', ['pr'], AGG_PERIODS],
    # ['annualMean', ['tas', 'rsds'], AGG_PERIODS],  # , 'rsds'
     ['annualMeanRainyDay', ['pr'], AGG_PERIODS],
    # ['monthlyClimatologicalMean',['pr', 'tasmin','tas',  'tasmax', 'rsds', 'wind'] , ['ann']],  # 'rsds','tas', ['pr', 'tasmin','tas',  'tasmax', 'rsds', 'wind']
    # ['annualRainyDays', ['pr'], AGG_PERIODS],
    # ['annualHotDays', ['tasmax'], AGG_PERIODS],
    # ['annualExtremeRain30', ['pr'], AGG_PERIODS],
    # ['annualExtremeRain50', ['pr'], AGG_PERIODS],
    # ['wetSpell10', ['pr'], AGG_PERIODS],
    # ['drySpell6', ['pr'], AGG_PERIODS],
    # ['annualMaxRain5dSum', ['pr'], AGG_PERIODS],
    # ['annualMaxRain3dSum', ['pr'], AGG_PERIODS],
    # ['annualMaxRain2dSum', ['pr'],AGG_PERIODS],
    # ['SPIxMonthly', ['pr'], AGG_PERIODS],
    # ['SPIbiannual', ['pr'], ['ann']],
    # ['onsetMarteau', ['pr'], ['mjjas']],
    #['pet', ['multivars'], AGG_PERIODS]
     ]

# NB: Currently excluding the following (but may add in later):
#            ['annualStrongWindDays', ['wind'], ['jas']]
#            ['annualHotDaysPerc', ['tasmax'], ['jas']],
#            ['annualRainyDaysPerc', ['pr'], ['jas']],
#            ['annualMaxRain5dMean', ['pr'], ['jas']],
#            ['annualMaxRain3dMean', ['pr'], ['jas']],
#            ['annualMaxRain2dMean', ['pr'], ['jas']],

# Plotnames: ['allModelRank', 'mapPerc', 'nbModelHistogram', 'MultiNbModelHistogram', 'allModelBoxplot', 'lineplot', 'allModelHisto']
# Plottypes: ['rcp26PercentageAnomaly', 'rcp26Anomaly', 'rcp26', 'rcp45PercentageAnomaly', 'rcp45Anomaly', 'rcp45', 'rcp85PercentageAnomaly', 'rcp85Anomaly', 'rcp85', 'scenarios', 'historical', 'percentageAnomaly', 'anomaly', 'allscen']


PLOTS_TOEXCLUDE = [
        #[metric, var, seas, reg, pn, pt]
    ['annualMax', ['pr', 'rsds'], ['all'], ['all'], ['all'],
     ['rcp26Anomaly', 'rcp26', 'rcp45Anomaly', 'rcp45', 'rcp85Anomaly', 'rcp85', 'anomaly']],

    ['annualTotalRain', ['pr'], ['all'], ['all'], ['all'],
     ['rcp26Anomaly', 'rcp26', 'rcp45Anomaly', 'rcp45', 'rcp85Anomaly', 'rcp85',  'anomaly']],

    ['annualMean', ['rsds'], ['all'], ['all'], ['all'],
     ['rcp26Anomaly', 'rcp26', 'rcp45Anomaly', 'rcp45', 'rcp85Anomaly', 'rcp85',  'anomaly']],

    ['annualMeanRainyDay', ['pr'], ['all'], ['all'], ['all'],
     ['rcp26Anomaly', 'rcp26', 'rcp45Anomaly', 'rcp45', 'rcp85Anomaly', 'rcp85',  'anomaly']],

    ['monthlyClimatologicalMean', ['rsds', 'wind'], ['all'], ['all'], ['all'],
     ['rcp26Anomaly', 'rcp26', 'rcp45Anomaly', 'rcp45', 'rcp85Anomaly', 'rcp85', 'anomaly']],

    ['annualRainyDays', ['pr'], ['all'], ['all'], ['all'],
     ['rcp26PercentageAnomaly', 'rcp26', 'rcp45PercentageAnomaly', 'rcp45', 'rcp85PercentageAnomaly', 'rcp85', 'percentageAnomaly']],

    ['annualExtremeRain30', ['pr'], ['all'], ['all'], ['all'],
     ['rcp26PercentageAnomaly', 'rcp26', 'rcp45PercentageAnomaly', 'rcp45', 'rcp85PercentageAnomaly', 'rcp85', 'percentageAnomaly']],

    ['annualExtremeRain50', ['pr'], ['all'], ['all'], ['all'],
     ['rcp26PercentageAnomaly', 'rcp26', 'rcp45PercentageAnomaly', 'rcp45', 'rcp85PercentageAnomaly', 'rcp85', 'percentageAnomaly']],

    ['annualExtremeRain100', ['pr'], ['all'], ['all'], ['all'],
     ['rcp26PercentageAnomaly', 'rcp26', 'rcp45PercentageAnomaly', 'rcp45', 'rcp85PercentageAnomaly', 'rcp85', 'percentageAnomaly']],

    ['wetSpell10', ['pr'], ['all'], ['all'], ['all'],
     ['rcp26PercentageAnomaly', 'rcp26', 'rcp45PercentageAnomaly', 'rcp45', 'rcp85PercentageAnomaly', 'rcp85', 'percentageAnomaly']],

    ['drySpell6', ['pr'], ['all'], ['all'], ['all'],
     ['rcp26PercentageAnomaly', 'rcp26', 'rcp45PercentageAnomaly', 'rcp45', 'rcp85PercentageAnomaly', 'rcp85', 'percentageAnomaly']],

    ['annualMaxRain5dSum', ['pr'], ['all'], ['all'], ['all'],
     ['rcp26Anomaly', 'rcp26', 'rcp45Anomaly', 'rcp45', 'rcp85Anomaly', 'rcp85',  'anomaly']],

    ['annualMaxRain3dSum', ['pr'], ['all'], ['all'], ['all'],
     ['rcp26Anomaly', 'rcp26', 'rcp45Anomaly', 'rcp45', 'rcp85Anomaly', 'rcp85',  'anomaly']],

    ['annualMaxRain2dSum', ['pr'], ['all'], ['all'], ['all'],
     ['rcp26Anomaly', 'rcp26', 'rcp45Anomaly', 'rcp45', 'rcp85Anomaly', 'rcp85',  'anomaly']],

    ['SPIxMonthly', ['pr'], ['all'], ['all'], ['all'],
     ['rcp26PercentageAnomaly', 'rcp26', 'rcp45PercentageAnomaly', 'rcp45', 'rcp85PercentageAnomaly', 'rcp85', 'percentageAnomaly']],

    ['SPIbiannual', ['pr'], ['all'], ['all'], ['all'],
     ['rcp26PercentageAnomaly', 'rcp26', 'rcp45PercentageAnomaly', 'rcp45', 'rcp85PercentageAnomaly', 'rcp85', 'percentageAnomaly']],

    ['onsetMarteau', ['pr'], ['all'], ['all'], ['all'],
     ['rcp26PercentageAnomaly', 'rcp26', 'rcp45PercentageAnomaly', 'rcp45', 'rcp85PercentageAnomaly', 'rcp85', 'percentageAnomaly']],

    ['pet', ['multivars'], ['all'], ['all'], ['all'],
     ['rcp26Anomaly', 'rcp26', 'rcp45Anomaly', 'rcp45', 'rcp85Anomaly', 'rcp85',  'anomaly']],
]

SINGLE_SCEN_PLOT = ['historical','rcp85'] #  run plot only for certain scenarios - reduces plot number'