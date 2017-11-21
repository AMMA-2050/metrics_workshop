# encoding: utf-8
'''
Contains functions to create labels in all types of plots
'''
import constants as cnst
import pdb

DC = '$^\circ$C'

METRICLONGNAME = {'ENGLISH' : {
            'annualMax' : 'Maximum',
            'annualMin' : 'Minimum',
            'annualTotalRain' : 'Total Rainfall',
            'annualMean' : 'Average',
            'annualMeanRainyDay' : 'Mean Daily Rainfall on Rainy Days',
            'monthlyClimatologicalMean' : 'Monthly Climatological Mean',
            'annualHotDaysPerc' : 'Percentage of Hot Days (Max Temp $>$'+str(cnst.HOTDAYS_THRESHOLD)+DC,
            'annualRainyDays' : 'Number of Rainy Days ($>$'+str(cnst.RAINYDAY_THRESHOLD)+'mm day$^{-1}$)',
            'annualRainyDaysPerc' : 'Percentage of Days that are Rainy ($>$'+str(cnst.RAINYDAY_THRESHOLD)+'mm day$^{-1}$)',
            'annualHotDays' : 'Number of Days with a Maximum Temperature $>$ '+str(cnst.HOTDAYS_THRESHOLD)+DC,
            'annualExtremeRain30' : 'Number of Days with Rainfall $>$ 30mm day$^{-1}$',
            'annualExtremeRain50' : 'Number of Days with Rainfall $>$ 50mm day$^{-1}$',
            'annualExtremeRain100' : 'Number of Days with Rainfall $>$ 100mm day$^{-1}$',
            'annualStrongWindDays' : 'Number of Days with Mean Wind Speed $>$ '+str(cnst.STRONGWIND_THRESHOLD),
            'wetSpell10': 'Number of Periods with a Wet Spell Longer Than 10 Days',
            'drySpell6': 'Number of Periods with a Dry Spell Longer Than 6 Days',
            'annualMaxRain5dSum': 'Maximum Rainfall Total in a 5-day Period',
            'annualMaxRain3dSum' : 'Maximum Rainfall Total in a 3-day Period',
            'annualMaxRain2dSum' : 'Maximum Rainfall Total in a 2-day Period',
            'annualMaxRain5dMean': 'Maximum Rainfall in a 5-day Period (Mean Daily Rate)',
            'annualMaxRain3dMean': 'Maximum Rainfall in a 3-day Period (Mean Daily Rate)',
            'annualMaxRain2dMean': 'Maximum Rainfall in a 2-day Period (Mean Daily Rate)',
            'SPIxMonthly' : 'Standardised Precipitation Index',
            'SPIbiannual' : 'Standardised Precipitation Index (bi-annual)',
            'onsetMarteau' : 'Local Agronomic Monsoon Onset Date (Marteau)',
            'cdd' : 'Consecutive Dry Days',
            'pet' : 'Potential Evapotranspiration'
    }, 
    'FRANCAIS' : {
            'annualMax' : 'Maximum',
            'annualMin' : 'Minimum',
            'annualTotalRain' : 'Précipitations totales',
            'annualMean' : 'Moyenne',
            'annualMeanRainyDay' : 'Précipitations moyennes par journée pluvieuse', # 'Mean Daily Rainfall on Rainy Days',
            'monthlyClimatologicalMean' : 'Moyenne climatologique mensuelle', #'Monthly Climatological Mean',
            'annualHotDaysPerc' : 'Pourcentage de journées chaudes (température maximale $>$'+str(cnst.HOTDAYS_THRESHOLD)+DC,# 'Percentage of Hot Days (Max Temp $>$'+str(cnst.HOTDAYS_THRESHOLD)+DC,
            'annualRainyDays' : 'Nombre de journées pluvieuses ($>$'+str(cnst.RAINYDAY_THRESHOLD)+' mm jour$^{-1}$)', #'Number of Rainy Days ($>$'+str(cnst.RAINYDAY_THRESHOLD)+'mm day$^{-1}$)',
            'annualRainyDaysPerc' : 'Pourcentage de journées pluvieuses ($>$'+str(cnst.RAINYDAY_THRESHOLD)+' mm jour$^{-1}$)', #'Percentage of Days that are Rainy ($>$'+str(cnst.RAINYDAY_THRESHOLD)+'mm day$^{-1}$)',
            'annualHotDays' : 'Nombre de journées avec une température maximale  $>$ '+str(cnst.HOTDAYS_THRESHOLD)+DC, #'Number of Days with a Maximum Temperature $>$ '+str(cnst.HOTDAYS_THRESHOLD)+DC,
            'annualExtremeRain30' : 'Nombre de journées avec précipitations $>$ 30 mm jour$^{-1}$', #'Number of Days with Rainfall $>$ 30mm day$^{-1}$',
            'annualExtremeRain50' : 'Nombre de journées avec précipitations $>$ 50 mm jour$^{-1}$', #'Number of Days with Rainfall $>$ 50mm day$^{-1}$',
            'annualExtremeRain100' : 'Nombre de journées avec précipitations $>$ 100 mm jour$^{-1}$', #'Number of Days with Rainfall $>$ 100mm day$^{-1}$',
            'annualStrongWindDays' : 'Nombre de journées avec un vent moyen $>$ '+str(cnst.STRONGWIND_THRESHOLD), #'Number of Days with Mean Wind Speed > '+str(cnst.STRONGWIND_THRESHOLD),
            'wetSpell10': 'Nombre de périodes pluvieuse de plus de 10 jours', #'Number of Periods with a Wet Spell Longer Than 10 Days',
            'drySpell6': 'Nombre de périodes sèches de plus de 6 jours', #'Number of Periods with a Dry Spell Longer Than 6 Days',
            'annualMaxRain5dSum': 'Précipitations maximum totales dans une période de 5 jours', #'Maximum Rainfall Total in a 5-day Period',
            'annualMaxRain3dSum' : 'Précipitations maximum totales dans une période de 3 jours',
            'annualMaxRain2dSum' : 'Précipitations maximum totales dans une période de 2 jours',
            'annualMaxRain5dMean': 'Précipitations maximum dans une période de 5 jours (taux moyenne quotidien)', #'Maximum Rainfall in a 5-day Period (Mean Daily Rate)',
            'annualMaxRain3dMean': 'Précipitations maximum dans une période de 3 jours (taux moyenne quotidien)', #'Maximum Rainfall in a 3-day Period (Mean Daily Rate)',
            'annualMaxRain2dMean': 'Précipitations maximum dans une période de 2 jours (taux moyenne quotidien)', #'Maximum Rainfall in a 2-day Period (Mean Daily Rate)',
            'SPIxMonthly' : 'Indice des précipitations standardisées',# 'Standardised Precipitation Index',
            'SPIbiannual' : 'Indice des précipitations standardisées (bi-annuelle)',
            'onsetMarteau' : 'Date de début de la mousson (agronomie locale ; Marteau)', # 'Local Agronomic Monsoon Onset Date (Marteau)',
            'cdd' : 'Nombre de journées sèches consécutives', #'Consecutive Dry Days',
            'pet' : 'Evapotranspiration potentielle' #'Potential Evapotranspiration'
            }
    }

MONTHS = [  'jan', 'feb', 'mar', 'apr','may', 'jun', 'jul', 'aug', 'sep','oct', 'nov','dec']


def getTitle(m, v, seas, scen, bc, r, anom=None):
    
    metvar = m + '_' + v
    
    if type(scen) == list:
        scen = ''
    else:
        scen = scen + '; '
    
    if anom in ['percentage', 'percentageAnomaly']:
        atxt = '% change in ' if cnst.LANGUAGE == 'ENGLISH' else 'Changements (%) '
    elif anom in ['absolute', 'anomaly']:
        atxt = 'Change in ' if cnst.LANGUAGE == 'ENGLISH' else 'Changements '
    elif anom in ['scenarios']:
        # This covers the case for multi-scenario boxplots, and possibly others
        scen = ''
        atxt = ''
    else:
        atxt = ''
    
    # e.g. Burkina Faso: Number of days when daily maximum temperature exceeds 40C (JAS)
    metricname= METRICLONGNAME[cnst.LANGUAGE][m]
    varname = cnst.VARNAMES[cnst.LANGUAGE][v].title()
    
    atxt, metricname = deFunction(atxt, metricname, cnst.LANGUAGE) # Changes de to du/de/de la/des/de l' and removes capitalisation
    
    
    titleLUT = {'ENGLISH' : {
            'annualMax_pr' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+seas+'; '+scen+bc+')',
            'annualMax_tasmax' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+seas+'; '+scen+bc+')',
            'annualMax_rsds' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+seas+'; '+scen+bc+')',
            'annualMin_tasmin' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+seas+'; '+scen+bc+')',
            'annualMean_tas' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+seas+'; '+scen+bc+')',
            'annualMean_rsds' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+seas+'; '+scen+bc+')',
            'monthlyClimatologicalMean_pr' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+seas+'; '+scen+bc+')',
            'monthlyClimatologicalMean_tasmin' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+seas+'; '+scen+bc+')',
            'monthlyClimatologicalMean_tas' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+seas+'; '+scen+bc+')',
            'monthlyClimatologicalMean_tasmax' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+seas+'; '+scen+bc+')',
            'monthlyClimatologicalMean_rsds' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+seas+'; '+scen+bc+')',
            'monthlyClimatologicalMean_wind' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+seas+'; '+scen+bc+')'
            },
            'FRANCAIS' : {
            'annualMax_pr' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+seas+' ; '+scen+bc+')',
            'annualMax_tasmax' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+seas+' ; '+scen+bc+')',
            'annualMax_rsds' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+seas+' ; '+scen+bc+')',
            'annualMin_tasmin' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+seas+' ; '+scen+bc+')',
            'annualMean_tas' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+seas+' ; '+scen+bc+')',
            'annualMean_rsds' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+seas+' ; '+scen+bc+')',
            'monthlyClimatologicalMean_pr' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+seas+' ; '+scen+bc+')',
            'monthlyClimatologicalMean_tasmin' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+seas+' ; '+scen+bc+')',
            'monthlyClimatologicalMean_tas' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+seas+' ; '+scen+bc+')',
            'monthlyClimatologicalMean_tasmax' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+seas+' ; '+scen+bc+')',
            'monthlyClimatologicalMean_rsds' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+seas+' ; '+scen+bc+')',
            'monthlyClimatologicalMean_wind' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+seas+' ; '+scen+bc+')'
            }
            }

    try:
        return(titleLUT[cnst.LANGUAGE][metvar])
    except:
        temp_title = r + ': ' + atxt + metricname + '\n('+seas+'; '+scen+bc+')'
        return(temp_title)

def getUnit(var):

    vardic = {'ENGLISH' : {
        'pr': '(mm day$^{-1}$)',
        'tasmax': '('+DC+')' ,
        'rsds': '(W m$^{-2}$)',
        'tasmin': '(' + DC + ')',
        'tas': '(' + DC + ')',
        'wind': '(m s$^{-1}$)',
        'multivars' : '(mm day$^{-1}$)'
        },
        'FRANCAIS' : {
        'pr': '(mm jour$^{-1}$)',
        'tasmax': '('+DC+')' ,
        'rsds': '(W m$^{-2}$)',
        'tasmin': '(' + DC + ')',
        'tas': '(' + DC + ')',
        'wind': '(m s$^{-1}$)',
        'multivars' : '(mm jour$^{-1}$)'
        }
        }

    return vardic[cnst.LANGUAGE][var]


def getYlab(m, v, anom=None):
    
    metvar = m + '_' + v
    
    ylabLUT_metvar = {'ENGLISH' : {
            'annualMax_pr' : 'Precipitation (mm day$^{-1}$)',
            'annualMax_tasmax' : 'Daily Max Temperature ('+DC+')',
            'annualMax_rsds' : 'SW Incoming Radiation (W m$^{-2}$)',
            'annualMin_tasmin' : 'Daily Min Temperature ('+DC+')',
            'annualMean_tas' : 'Daily Mean Temperature ('+DC+')',
            'annualMean_rsds' : 'SW Incoming Radiation (W m$^{-2}$)',
            'monthlyClimatologicalMean_pr' : 'Precipitation (mm day$^{-1}$)',
            'monthlyClimatologicalMean_tasmin' : 'Daily Min Temperature ('+DC+')',
            'monthlyClimatologicalMean_tas' : 'Daily Mean Temperature ('+DC+')',
            'monthlyClimatologicalMean_tasmax' : 'Daily Max Temperature ('+DC+')',
            'monthlyClimatologicalMean_rsds' : 'SW Incoming Radiation (W m$^{-2}$)',
            'monthlyClimatologicalMean_wind' : 'Wind Speed (m s$^{-1}$)'
            },
            'FRANCAIS' : {
            'annualMax_pr' : 'Precipitation (mm day$^{-1}$)',
            'annualMax_tasmax' : 'Daily Max Temperature ('+DC+')',
            'annualMax_rsds' : 'SW Incoming Radiation (W m$^{-2}$)',
            'annualMin_tasmin' : 'Daily Min Temperature ('+DC+')',
            'annualMean_tas' : 'Daily Mean Temperature ('+DC+')',
            'annualMean_rsds' : 'SW Incoming Radiation (W m$^{-2}$)',
            'monthlyClimatologicalMean_pr' : 'Precipitation (mm day$^{-1}$)',
            'monthlyClimatologicalMean_tasmin' : 'Daily Min Temperature ('+DC+')',
            'monthlyClimatologicalMean_tas' : 'Daily Mean Temperature ('+DC+')',
            'monthlyClimatologicalMean_tasmax' : 'Daily Max Temperature ('+DC+')',
            'monthlyClimatologicalMean_rsds' : 'SW Incoming Radiation (W m$^{-2}$)',
            'monthlyClimatologicalMean_wind' : 'Wind Speed (m s$^{-1}$)'
            }
            }
    
    ylabLUT = {'ENGLISH' : {
            'annualTotalRain' : 'Precipitation (mm)',
            'annualMeanRainyDay' : 'Precipitation (mm)',
            'annualHotDaysPerc' : 'No. of Days', #when Max Temp >'+str(cnst.HOTDAYS_THRESHOLD)+'$^{\circ}$C',
            'annualRainyDays' : 'No. of Rainy Days', # (>'+str(cnst.RAINYDAY_THRESHOLD)+'mm day$^{-1}$)',
            'annualRainyDaysPerc' : 'No. of Rainy Days', # (>'+str(cnst.RAINYDAY_THRESHOLD)+'mm day$^{-1}$)',
            'annualHotDays' : 'No. of Days', # when Max Temp >'+str(cnst.HOTDAYS_THRESHOLD)+'$^{\circ}$C',
            'annualExtremeRain30' : 'No. of Days', # > 30mm day$^{-1}$',
            'annualExtremeRain50' : 'No. of Days', # > 50mm day$^{-1}$',
            'annualExtremeRain100' : 'No. of Days', # > 100mm day$^{-1}$',
            'annualStrongWindDays' : 'No. of Days', # >'+str(cnst.STRONGWIND_THRESHOLD)+'ms$^{-1}$',
            'wetSpell10': 'No. of Wet Periods', # > 10 Days',
            'drySpell6': 'No. of Dry Periods', # > 6 Days',
            'annualMaxRain_5dSum': '5-day Total Precipitation',
            'annualMaxRain_3dSum' : '3-day Total Precipitation',
            'annualMaxRain_2dSum' : '2-day Total Precipitation',
            'annualMaxRain_5dMean': '5-day Mean Precipitation Rate (mm day$^{-1}$)',
            'annualMaxRain_3dMean': '3-day Mean Precipitation Rate (mm day$^{-1}$)',
            'annualMaxRain_2dMean': '2-day Mean Precipitation Rate (mm day$^{-1}$)',
            'SPIxMonthly' : 'SPI',
            'SPIbiannual' : 'SPI (bi-annual)',
            'onsetMarteau' : 'Julian Day',
            'cdd' : 'Consecutive Dry Days',
            'pet' : 'PET (mm day$^{-1}$)'
            },
            'FRANCAIS' : {
            'annualTotalRain' : 'Précipitations (mm)',
            'annualMeanRainyDay' : 'Précipitations (mm)',
            'annualHotDaysPerc' : 'No. de jours', #when Max Temp >'+str(cnst.HOTDAYS_THRESHOLD)+'$^{\circ}$C',
            'annualRainyDays' : 'No. of Rainy Days', # (>'+str(cnst.RAINYDAY_THRESHOLD)+'mm day$^{-1}$)',
            'annualRainyDaysPerc' : 'No. of Rainy Days', # (>'+str(cnst.RAINYDAY_THRESHOLD)+'mm day$^{-1}$)',
            'annualHotDays' : 'No. of Days', # when Max Temp >'+str(cnst.HOTDAYS_THRESHOLD)+'$^{\circ}$C',
            'annualExtremeRain30' : 'No. of Days', # > 30mm day$^{-1}$',
            'annualExtremeRain50' : 'No. of Days', # > 50mm day$^{-1}$',
            'annualExtremeRain100' : 'No. of Days', # > 100mm day$^{-1}$',
            'annualStrongWindDays' : 'No. of Days', # >'+str(cnst.STRONGWIND_THRESHOLD)+'ms$^{-1}$',
            'wetSpell10': 'No. of Wet Periods', # > 10 Days',
            'drySpell6': 'No. of Dry Periods', # > 6 Days',
            'annualMaxRain_5dSum': '5-day Total Precipitation',
            'annualMaxRain_3dSum' : '3-day Total Precipitation',
            'annualMaxRain_2dSum' : '2-day Total Precipitation',
            'annualMaxRain_5dMean': '5-day Mean Precipitation Rate (mm day$^{-1}$)',
            'annualMaxRain_3dMean': '3-day Mean Precipitation Rate (mm day$^{-1}$)',
            'annualMaxRain_2dMean': '2-day Mean Precipitation Rate (mm day$^{-1}$)',
            'SPIxMonthly' : 'SPI',
            'SPIbiannual' : 'SPI (bi-annual)',
            'onsetMarteau' : 'Julian Day',
            'cdd' : 'Consecutive Dry Days',
            'pet' : 'PET (mm day$^{-1}$)'
            }
            }
    
    try:
        if any([m in mykey for mykey in ylabLUT_metvar[cnst.LANGUAGE].keys()]):
            ylab = ylabLUT_metvar[cnst.LANGUAGE][metvar]
        else:
            ylab = ylabLUT[cnst.LANGUAGE][m]
    except:
        ylab = cnst.VARNAMES[cnst.LANGUAGE][v] + ': ' + m

    unit = getUnit(v)
    
    if anom in ['percentage', 'percentageAnomaly']:
        ylab = '% change ' if cnst.LANGUAGE == 'ENGLISH' else 'Changement (%) de '
    if anom in ['absolute', 'anomaly']:
        ylab = 'Absolute change '+unit if cnst.LANGUAGE == 'ENGLISH' else 'Changement absolut de '+unit
    
    return(ylab)

def getFigSize(region, plottype):
    
    if region:
        comb = plottype + '_' + region
    else:
        comb = plottype
    
    # (width, height)
    thisLUT = {'map_BF':(8,8),
               'map_SG': (8,8),
               'map_WA': (8,6),
               'nbModelHistogram': (8.5,6)
            }
    
    try:
        return(thisLUT[comb])
    except:
        return((9,9))