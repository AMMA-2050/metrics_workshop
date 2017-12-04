# encoding: utf-8

"""
Contains global constants for the CMIP5 atlas
"""

VERSION = '1.0'
LANGUAGE = 'FRANCAIS' # 'ENGLISH' # 'FRANCAIS'
DATADIR = '/project/FCFA/CMIP5/bias_corrected/WA_data' #'/users/global/cornkle/CMIP/CMIP5_Africa' #'/Users/ajh235/Work/DataLocal/Projects/AMMA-2050' #'/project/FCFA/CMIP5/bias_corrected/WA_data'

REGIONS = {'WA' : ['WA', 'West Africa' if LANGUAGE == 'ENGLISH' else "Afrique de l'Ouest", [-18, 25, 4, 25], 'WA_files'],   # lon1, lon2, lat1, lat2
           'BF' : ['BF', u'Burkina Faso',[-6, 2.8, 9 ,15.5], 'Burkina_files'],
           'SG' : ['SG', u'Senegal' if LANGUAGE == 'ENGLISH' else u'Sénégal', [-18, -11, 12, 17], 'Senegal_files'],
           'SH' : ['SH', u'Sahelian Zone' if LANGUAGE == 'ENGLISH' else u'Zone sahélienne', [-11, 30, 12.5, 17.5], 'Sahel_files'],
           'SD' : ['SD', u'Sudanian Zone' if LANGUAGE == 'ENGLISH' else u'Zone soudanienne', [-18, 30, 8, 12.5], 'Sudanian_files'],
           'GC' : ['GC', u'Guinea Coast Zone' if LANGUAGE == 'ENGLISH' else u'Zone de la côte guinéenne', [-15, 10, 3.5, 8], 'GuineaCoast_files']
           }
#### Atlas production / file creation is supporting only one region at a time
#ATLAS_REGION = REGIONS['SG']
ATLAS_REGION = REGIONS['SD']

METRIC_DATADIR = DATADIR + '/metric_atlas/' + ATLAS_REGION[3] +'/save_files/netcdf'
METRIC_PLOTDIR = DATADIR + '/metric_atlas/' + ATLAS_REGION[3] + '/save_files/plots_' + LANGUAGE
METRIC_ATLASDIR = DATADIR + '/metric_atlas/' + ATLAS_REGION[3]
BC_RES = ['BC_0.5x0.5'] #'0.5x0.5'

SCENARIO = ['historical', 'rcp26', 'rcp45', 'rcp85'] 

AGGREGATION = ['tseries', '2d', 'trend']

FTYPES = ['singleModels', 'allModels', 'anomalies', 'anomaliesPerc']

VARNAMES = {'ENGLISH' : {'pr' : u'daily precipitation',
            'tas' : u'daily mean temperature',
            'tasmin' : u'daily minimum temperature',
            'tasmax' : u'daily maximum temperature',
            'rsds' : u'surface downwelling shortwave radiation',
            'wind' : u'near surface wind speed',
            'multivars' : u'multiple input variables'
            },
            'FRANCAIS' :{'pr' : u'précipitations journalières',
            'tas' : u'température moyenne journalière',
            'tasmin' : u'température minimale journalière',
            'tasmax' : u'température maximale journalière',
            'rsds' : u'flux solaire entrant à la surface', #'descendant radiation à ondes courtes alla surface'
            'wind' : u'vitesse du vent près de la surface',
            'multivars' : u'multiple input variables' # needs to stay the same (not used in captions)
            }
            }

FUT_TREND = [2010, 2060]
FUTURE = [2040, 2059]
HIST = [1950, 2000]

HOTDAYS_THRESHOLD = 40
RAINYDAY_THRESHOLD = 1
STRONGWIND_THRESHOLD = 10 # Values in 1 sample file have a historical max of 7 to 9, so this value is still far too high


OVERWRITE = 'Yes' # 'Yes'


#######################################
# Choose metric specific options
#######################################
# metric: exact name as appears in calc.py as a character string
# variable: list of climate variable(s) to send to the calc function
# season: list of seasons to run the metric-variable combination for

## SPIbiannual, monthlyClimatologicalMean and onsetMarteau are exceptions to the atlas aggregation period!
## Their aggregation period never changes.


if ATLAS_REGION[0] == 'GC':
    AGG_PERIODS = ['jas', 'may', 'jun', 'jul','aug','sep','oct','nov']
else:
    AGG_PERIODS = ['jas', 'jun', 'jul','aug','sep','oct'] # ['jas', 'may', 'jun', 'jul','aug','sep','oct','nov']

CONSTANT_PERIOD_METRIC = ['onsetMarteau', 'SPIbiannual', 'monthlyClimatologicalMean']
### slowest variables go first!

METRICS_TORUN = [
#    ['pet', ['multivars'], AGG_PERIODS],
#    ['onsetMarteau', ['pr'], ['mjjas']],
#    ['SPIxMonthly', ['pr'], AGG_PERIODS],
#    ['SPIbiannual', ['pr'], ['ann']],
#    ['wetSpell10', ['pr'], AGG_PERIODS],
#    ['drySpell6', ['pr'], AGG_PERIODS],
    ['annualMax', ['pr', 'tasmax', 'rsds'], AGG_PERIODS],
#    ['annualMin', ['tasmin'], AGG_PERIODS],
#    ['annualTotalRain', ['pr'], AGG_PERIODS],
#    ['annualMean', ['tas', 'rsds'], AGG_PERIODS],
#    ['annualMeanRainyDay', ['pr'], AGG_PERIODS],
#    ['monthlyClimatologicalMean', ['pr', 'tasmin', 'tas', 'tasmax', 'rsds', 'wind'], ['ann']],
#    ['annualRainyDays', ['pr'], AGG_PERIODS],
#    ['annualHotDays', ['tasmax'], AGG_PERIODS],
#    ['annualExtremeRain30', ['pr'], AGG_PERIODS],
#    ['annualExtremeRain50', ['pr'], AGG_PERIODS],
#    ['annualMaxRain5dSum', ['pr'], AGG_PERIODS],
#    ['annualMaxRain3dSum', ['pr'], AGG_PERIODS],
#    ['annualMaxRain2dSum', ['pr'], AGG_PERIODS]
]

# NB: Currently excluding the following (but may add in later):
#            ['annualStrongWindDays', ['wind'], ['jas']]
#            ['annualHotDaysPerc', ['tasmax'], ['jas']],
#            ['annualRainyDaysPerc', ['pr'], ['jas']],
#            ['annualMaxRain5dMean', ['pr'], ['jas']],
#            ['annualMaxRain3dMean', ['pr'], ['jas']],
#            ['annualMaxRain2dMean', ['pr'], ['jas']],


#  Define scenarios for which to run single scenario plots
#  No single scenario plots produced for rcp45 and rcp26 at the moment.
SINGLE_SCEN_PLOT = ['historical','rcp85']


# To exclude certain produced plots from the atlas
# Plotnames: ['allModelRank', 'mapPerc', 'nbModelHistogram', 'MultiNbModelHistogram', 'allModelBoxplot', 'lineplot', 'allModelHisto']
# Plottypes: ['rcp26PercentageAnomaly', 'rcp26Anomaly', 'rcp26', 'rcp45PercentageAnomaly', 'rcp45Anomaly', 'rcp45', 'rcp85PercentageAnomaly', 'rcp85Anomaly', 'rcp85', 'scenarios', 'historical', 'percentageAnomaly', 'anomaly', 'allscen']
PLOTS_TOEXCLUDE = [
    #[metric, variable, season, region, plotname, plottype]
    ['annualMax', ['pr', 'rsds'], ['all'], ['all'], ['all'],
     ['rcp26Anomaly', 'rcp26', 'rcp45Anomaly', 'rcp45', 'rcp85Anomaly', 'rcp85', 'anomaly']],

    ['annualTotalRain', ['pr'], ['all'], ['all'], ['all'],
     ['rcp26Anomaly', 'rcp26', 'rcp45Anomaly', 'rcp45', 'rcp85Anomaly', 'rcp85',  'anomaly']],

    ['annualMean', ['rsds'], ['all'], ['all'], ['all'],
     ['rcp26Anomaly', 'rcp26', 'rcp45Anomaly', 'rcp45', 'rcp85Anomaly', 'rcp85',  'anomaly']],

    ['annualMeanRainyDay', ['pr'], ['all'], ['all'], ['all'],
     ['rcp26Anomaly', 'rcp26', 'rcp45Anomaly', 'rcp45', 'rcp85Anomaly', 'rcp85',  'anomaly']],

    ['monthlyClimatologicalMean', ['rsds', 'wind'], ['all'], ['all'], ['all'],
     ['rcp26Anomaly', 'rcp26', 'rcp45Anomaly', 'rcp45', 'rcp85Anomaly', 'rcp85']],

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


### This is only used by the plot routines to make sure all expected aggregations are available (error check)
METRIC_AGGS = {
            'annualMax' : ['tseries', '2d'],
            'annualMin' : ['tseries', '2d'],
            'annualTotalRain' : ['tseries', '2d'],
            'annualMean' : ['tseries', '2d'],
            'annualMeanRainyDay' : ['tseries', '2d'],
            'monthlyClimatologicalMean' : ['tseries'],
            'annualHotDaysPerc' : ['tseries', '2d'],
            'annualRainyDays' : ['tseries', '2d'],
            'annualRainyDaysPerc' : ['tseries', '2d'],
            'annualHotDays' : ['tseries', '2d'],
            'annualExtremeRain30' : ['tseries', '2d'],
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
