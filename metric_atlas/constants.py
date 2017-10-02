"""
Contains global constants for the CMIP5 atlas
"""
VERSION = 'v0.2.2'
DATADIR = '/project/FCFA/CMIP5/bias_corrected/WA_data' #'/users/global/cornkle/CMIP/CMIP5_Africa' #'/Users/ajh235/Work/DataLocal/Projects/AMMA-2050' #'/project/FCFA/CMIP5/bias_corrected/WA_data'
METRIC_DATADIR = DATADIR + '/save_files/metric_data'
METRIC_PLOTDIR = DATADIR + '/save_files/metric_plots'
METRIC_ATLASDIR = DATADIR + '/save_files/metric_atlas'
BC_RES = ['BC_0.5x0.5'] #['0.5x0.5', 'BC_0.5x0.5', 'BC_mdlgrid', 'mdlgrid']

SCENARIO = ['historical', 'rcp85'] # ['historical', 'rcp85'] #['historical', 'rcp26', 'rcp45', 'rcp85']

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

# TODO @Conni: I ran the following metrics for all scenarios, and you will need to run the plotting script also for these scenarios:
#            ['annualMax', ['pr','tasmax', 'rsds'], ['jas']], # , 'rsds'
#            ['annualTotalRain', ['pr'], ['jas']]
# TODO @Conni: When running the whole atlas, you'll need to have METRICS_TORUN looking like below.
# TODO @Conni: The one thing I haven't figured out yet is how to do 'all scenarios' for certain plots (following Dave's request). Maybe we should say we can't do that for this version?

METRICS_TORUN = [
            ['pet', ['multivars'], ['jas']],
            ['annualMax', ['pr','tasmax', 'rsds'], ['jas']], # , 'rsds'
            ['annualMin', ['tasmin'], ['jas']],
            ['annualTotalRain', ['pr'], ['jas']],
            ['annualMean', ['tas', 'rsds'], ['jas']], # , 'rsds'
            ['annualMeanRainyDay', ['pr'], ['jas']],
            ['monthlyClimatologicalMean', ['pr', 'tasmin', 'tas', 'tasmax', 'rsds', 'wind'], ['jas']], # 'rsds', 
            ['annualRainyDays', ['pr'], ['jas']],
            ['annualHotDays', ['tasmax'], ['jas']],
            ['annualExtremeRain30', ['pr'], ['jas']],
            ['annualExtremeRain50', ['pr'], ['jas']],
            ['annualExtremeRain100', ['pr'], ['jas']],
            ['wetSpell10', ['pr'], ['jas']],
            ['drySpell6', ['pr'], ['jas']],
            ['annualMaxRain5dSum', ['pr'], ['jas']],
            ['annualMaxRain3dSum', ['pr'], ['jas']],
            ['annualMaxRain2dSum', ['pr'], ['jas']],
            ['SPIxMonthly', ['pr'], ['jas']],
            ['SPIbiannual', ['pr'], ['ann']],
            ['onsetMarteau', ['pr'], ['mjjas']]
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

# TODO @Conni: Add in more exceptions below
PLOTS_TOEXCLUDE = [
        #[metric, var, seas, reg, pn, pt]
        ['annualMax', ['pr', 'rsds'], ['all'], ['all'], ['all'], ['rcp26Anomaly', 'rcp26', 'rcp45Anomaly', 'rcp45', 'rcp85Anomaly', 'rcp85', 'scenarios', 'percentageAnomaly', 'anomaly', 'allscen']],
        ['annualMax', ['tas'], ['all'], ['all'], ['all'], ['rcp26PercentageAnomaly', 'rcp26', 'rcp45PercentageAnomaly', 'rcp45', 'rcp85PercentageAnomaly', 'rcp85', 'scenarios', 'percentageAnomaly', 'anomaly', 'allscen']],
        
        
        ]