# encoding: utf-8
'''
Contains functions to create labels in all types of plots
'''
import constants as cnst
import createAtlas as ca
import pdb

DC = '$^\circ$C'

METRICLONGNAME = {'ENGLISH' : {
            'annualMax' : u'Maximum',
            'annualMin' : u'Minimum',
            'annualTotalRain' : u'Total Rainfall',
            'annualMean' : u'Average',
            'annualMeanRainyDay' : u'Mean Daily Rainfall on Rainy Days',
            'monthlyClimatologicalMean' : u'Monthly Climatological Mean',
            'annualHotDaysPerc' : u'Percentage of Hot Days (Max Temp $>$'+str(cnst.HOTDAYS_THRESHOLD)+DC,
            'annualRainyDays' : u'Number of Rainy Days ($>$'+str(cnst.RAINYDAY_THRESHOLD)+u'mm day$^{-1}$)',
            'annualRainyDaysPerc' : u'Percentage of Days that are Rainy ($>$'+str(cnst.RAINYDAY_THRESHOLD)+u'mm day$^{-1}$)',
            'annualHotDays' : u'Number of Days with a Maximum Temperature $>$ '+str(cnst.HOTDAYS_THRESHOLD)+DC,
            'annualExtremeRain30' : u'Number of Days with Rainfall $>$ 30mm day$^{-1}$',
            'annualExtremeRain50' : u'Number of Days with Rainfall $>$ 50mm day$^{-1}$',
            'annualExtremeRain100' : u'Number of Days with Rainfall $>$ 100mm day$^{-1}$',
            'annualStrongWindDays' : u'Number of Days with Mean Wind Speed $>$ '+str(cnst.STRONGWIND_THRESHOLD),
            'wetSpell10': u'Number of Periods with a Wet Spell Longer Than 10 Days',
            'drySpell6': u'Number of Periods with a Dry Spell Longer Than 6 Days',
            'annualMaxRain5dSum': u'Maximum Rainfall Total in a 5-day Period',
            'annualMaxRain3dSum' : u'Maximum Rainfall Total in a 3-day Period',
            'annualMaxRain2dSum' : u'Maximum Rainfall Total in a 2-day Period',
            'annualMaxRain5dMean': u'Maximum Rainfall in a 5-day Period (Mean Daily Rate)',
            'annualMaxRain3dMean': u'Maximum Rainfall in a 3-day Period (Mean Daily Rate)',
            'annualMaxRain2dMean': u'Maximum Rainfall in a 2-day Period (Mean Daily Rate)',
            'SPIxMonthly' : u'Standardised Precipitation Index',
            'SPIbiannual' : u'Standardised Precipitation Index (bi-annual)',
            'onsetMarteau' : u'Local Agronomic Monsoon Onset Date (Marteau)',
            'cdd' : u'Consecutive Dry Days',
            'pet' : u'Potential Evapotranspiration'
    }, 
    'FRANCAIS' : {
            'annualMax' : u'Maximale de',
            'annualMin' : u'Minimale de',
            'annualTotalRain' : u'Précipitations totales',
            'annualMean' : u'Moyenne',
            'annualMeanRainyDay' : u'Précipitations moyennes par journée pluvieuse', # 'Mean Daily Rainfall on Rainy Days',
            'monthlyClimatologicalMean' : u'Moyenne climatologique mensuelle', #'Monthly Climatological Mean',
            'annualHotDaysPerc' : u'Pourcentage de journées chaudes (température maximale $>$'+str(cnst.HOTDAYS_THRESHOLD)+DC,# 'Percentage of Hot Days (Max Temp $>$'+str(cnst.HOTDAYS_THRESHOLD)+DC,
            'annualRainyDays' : u'Nombre de journées pluvieuses ($>$'+str(cnst.RAINYDAY_THRESHOLD)+u' mm jour$^{-1}$)', #'Number of Rainy Days ($>$'+str(cnst.RAINYDAY_THRESHOLD)+'mm day$^{-1}$)',
            'annualRainyDaysPerc' : u'Pourcentage de journées pluvieuses ($>$'+str(cnst.RAINYDAY_THRESHOLD)+u' mm jour$^{-1}$)', #'Percentage of Days that are Rainy ($>$'+str(cnst.RAINYDAY_THRESHOLD)+'mm day$^{-1}$)',
            'annualHotDays' : u'Nombre de journées avec une température maximale  $>$ '+str(cnst.HOTDAYS_THRESHOLD)+DC, #'Number of Days with a Maximum Temperature $>$ '+str(cnst.HOTDAYS_THRESHOLD)+DC,
            'annualExtremeRain30' : u'Nombre de journées avec précipitations $>$ 30 mm jour$^{-1}$', #'Number of Days with Rainfall $>$ 30mm day$^{-1}$',
            'annualExtremeRain50' : u'Nombre de journées avec précipitations $>$ 50 mm jour$^{-1}$', #'Number of Days with Rainfall $>$ 50mm day$^{-1}$',
            'annualExtremeRain100' : u'Nombre de journées avec précipitations $>$ 100 mm jour$^{-1}$', #'Number of Days with Rainfall $>$ 100mm day$^{-1}$',
            'annualStrongWindDays' : u'Nombre de journées avec un vent moyen $>$ '+str(cnst.STRONGWIND_THRESHOLD), #'Number of Days with Mean Wind Speed > '+str(cnst.STRONGWIND_THRESHOLD),
            'wetSpell10': u'Nombre de périodes pluvieuse de plus de 10 jours', #'Number of Periods with a Wet Spell Longer Than 10 Days',
            'drySpell6': u'Nombre de périodes sèches de plus de 6 jours', #'Number of Periods with a Dry Spell Longer Than 6 Days',
            'annualMaxRain5dSum': u'Précipitations maximum totales dans une période de 5 jours', #'Maximum Rainfall Total in a 5-day Period',
            'annualMaxRain3dSum' : u'Précipitations maximum totales dans une période de 3 jours',
            'annualMaxRain2dSum' : u'Précipitations maximum totales dans une période de 2 jours',
            'annualMaxRain5dMean': u'Précipitations maximum dans une période de 5 jours (taux moyenne quotidien)', #'Maximum Rainfall in a 5-day Period (Mean Daily Rate)',
            'annualMaxRain3dMean': u'Précipitations maximum dans une période de 3 jours (taux moyenne quotidien)', #'Maximum Rainfall in a 3-day Period (Mean Daily Rate)',
            'annualMaxRain2dMean': u'Précipitations maximum dans une période de 2 jours (taux moyenne quotidien)', #'Maximum Rainfall in a 2-day Period (Mean Daily Rate)',
            'SPIxMonthly' : u'Indice normalisé de précipitations',# 'Standardised Precipitation Index',
            'SPIbiannual' : u'Indice normalisé de précipitations (bi-annuelle)',
            'onsetMarteau' : u'Date de déclenchement de la mousson (Marteau)', # 'Local Agronomic Monsoon Onset Date (Marteau)',
            'cdd' : u'Nombre de jours consécutifs sans précipitation', #'Consecutive Dry Days',
            'pet' : u'Evapotranspiration potentielle' #'Potential Evapotranspiration'
            }
    }

MONTHS = [  'jan', 'feb', 'mar', 'apr','may', 'jun', 'jul', 'aug', 'sep','oct', 'nov','dec']

def deFunction(atxt, metricname):
    
    if cnst.LANGUAGE == 'ENGLISH':
        atxt_new, metricname_new = [atxt, metricname]
    else:
        firstword = metricname.split(' ')[0]
        d = ' '
        print firstword
        if firstword in [u'Nombre', u'Pourcentage', u'Maximale']:
            d = u'du '
        if firstword in [u'Minimale']:
            d = u'de la '
        if firstword in [u'Précipitations']:
            d = u'des '
        if firstword in [u'Indice', u'Evapotranspiration']:
            d = u'd\''

        atxt_new, metricname_new = [atxt, d + metricname.lower()]
        
    return([atxt_new, metricname_new])
    
def getTitle(m, v, seas, scen, bc, r, anom=None):
    
    metvar = m + '_' + v
    
    if type(scen) == list:
        scen = ''
    else:
        scen = scen + '; '
    atxt = ''
    if anom in ['percentageAnomaly', 'PercentageAnomaly']:
        atxt = u'% change in ' if cnst.LANGUAGE == 'ENGLISH' else u'Changements (%) '
    if anom in ['absolute', 'Absolute', 'anomaly', 'Anomaly']:
        atxt = u'Change in ' if cnst.LANGUAGE == 'ENGLISH' else u'Changements '
    if anom in ['scenarios']:
        # This covers the case for multi-scenario boxplots, and possibly others
        scen = ''
        atxt = ''

    # e.g. Burkina Faso: Number of days when daily maximum temperature exceeds 40C (JAS)
    metricname= METRICLONGNAME[cnst.LANGUAGE][m]
    varname = cnst.VARNAMES[cnst.LANGUAGE][v].title()
    
    atxt, metricname = deFunction(atxt, metricname) # Changes de to du/de/de la/des/de l' and removes capitalisation
    
    titleLUT = {'ENGLISH' : {
            'annualMax_pr' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+'; '+scen+bc+')',
            'annualMax_tasmax' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+'; '+scen+bc+')',
            'annualMax_rsds' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+'; '+scen+bc+')',
            'annualMin_tasmin' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+'; '+scen+bc+')',
            'annualMean_tas' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+'; '+scen+bc+')',
            'annualMean_rsds' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+'; '+scen+bc+')',
            'monthlyClimatologicalMean_pr' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+'; '+scen+bc+')',
            'monthlyClimatologicalMean_tasmin' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+'; '+scen+bc+')',
            'monthlyClimatologicalMean_tas' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+'; '+scen+bc+')',
            'monthlyClimatologicalMean_tasmax' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+'; '+scen+bc+')',
            'monthlyClimatologicalMean_rsds' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+'; '+scen+bc+')',
            'monthlyClimatologicalMean_wind' : r + ': ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+'; '+scen+bc+')'
            },
            'FRANCAIS' : {
            'annualMax_pr' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+' ; '+scen+bc+')',
            'annualMax_tasmax' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+' ; '+scen+bc+')',
            'annualMax_rsds' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+' ; '+scen+bc+')',
            'annualMin_tasmin' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+' ; '+scen+bc+')',
            'annualMean_tas' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+' ; '+scen+bc+')',
            'annualMean_rsds' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+' ; '+scen+bc+')',
            'monthlyClimatologicalMean_pr' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+' ; '+scen+bc+')',
            'monthlyClimatologicalMean_tasmin' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+' ; '+scen+bc+')',
            'monthlyClimatologicalMean_tas' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+' ; '+scen+bc+')',
            'monthlyClimatologicalMean_tasmax' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+' ; '+scen+bc+')',
            'monthlyClimatologicalMean_rsds' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+' ; '+scen+bc+')',
            'monthlyClimatologicalMean_wind' : r + ' : ' + atxt + metricname + ' ' + varname + '\n('+ca.monthLookUp(seas)+' ; '+scen+bc+')'
            }
            }

    try:
        return(titleLUT[cnst.LANGUAGE][metvar])
    except KeyError:
        temp_title = r + ': ' + atxt + metricname.lower() + '\n('+ca.monthLookUp(seas)+'; '+scen+bc+')'
        return(temp_title)

def getUnit(var):

    vardic = {'ENGLISH' : {
        'pr': u'(mm day$^{-1}$)',
        'tasmax': u'('+DC+')' ,
        'rsds': u'(W m$^{-2}$)',
        'tasmin': u'(' + DC + u')',
        'tas': u'(' + DC + u')',
        'wind': u'(m s$^{-1}$)',
        'multivars' : u'(mm day$^{-1}$)'
        },
        'FRANCAIS' : {
        'pr': u'(mm jour$^{-1}$)',
        'tasmax': u'('+DC+')' ,
        'rsds': u'(W m$^{-2}$)',
        'tasmin': '(' + DC + ')',
        'tas': '(' + DC + ')',
        'wind': u'(m s$^{-1}$)',
        'multivars' : u'(mm jour$^{-1}$)'
        }
        }

    return vardic[cnst.LANGUAGE][var]


def getYlab(m, v, anom=None):
    
    metvar = m + '_' + v
    
    ylabLUT_metvar = {'ENGLISH' : {
            'annualMax_pr' : u'Precipitation (mm day$^{-1}$)',
            'annualMax_tasmax' : u'Daily Max Temperature ('+DC+')',
            'annualMax_rsds' : u'SW Incoming Radiation (W m$^{-2}$)',
            'annualMin_tasmin' : u'Daily Min Temperature ('+DC+')',
            'annualMean_tas' : u'Daily Mean Temperature ('+DC+')',
            'annualMean_rsds' : u'SW Incoming Radiation (W m$^{-2}$)',
            'monthlyClimatologicalMean_pr' : u'Precipitation (mm day$^{-1}$)',
            'monthlyClimatologicalMean_tasmin' : u'Daily Min Temperature ('+DC+')',
            'monthlyClimatologicalMean_tas' : u'Daily Mean Temperature ('+DC+')',
            'monthlyClimatologicalMean_tasmax' : u'Daily Max Temperature ('+DC+')',
            'monthlyClimatologicalMean_rsds' : u'SW Incoming Radiation (W m$^{-2}$)',
            'monthlyClimatologicalMean_wind' : u'Wind Speed (m s$^{-1}$)'
            },
            'FRANCAIS' : {
            'annualMax_pr' : u'Précipitations (mm jour$^{-1}$)',
            'annualMax_tasmax' : u'Température max. journalière ('+DC+')',
            'annualMax_rsds' : u'Flux solaire entrant à la surface (W m$^{-2}$)',
            'annualMin_tasmin' : u'Température min. journalière ('+DC+')',
            'annualMean_tas' : u'Température moyenne journalière ('+DC+')',
            'annualMean_rsds' : u'Flux solaire entrant à la surface (W m$^{-2}$)',
            'monthlyClimatologicalMean_pr' : u'Précipitations (mm jour$^{-1}$)',
            'monthlyClimatologicalMean_tasmin' : u'Température min. journalière ('+DC+')',
            'monthlyClimatologicalMean_tas' : u'Température moyenne journalière ('+DC+')',
            'monthlyClimatologicalMean_tasmax' : u'Température max. journalière ('+DC+')',
            'monthlyClimatologicalMean_rsds' : u'Flux solaire entrant à la surface (W m$^{-2}$)',
            'monthlyClimatologicalMean_wind' : u'Vitesse du vent (m s$^{-1}$)'
            }
            }
    
    ylabLUT = {'ENGLISH' : {
            'annualTotalRain' : u'Precipitation (mm)',
            'annualMeanRainyDay' : u'Precipitation (mm)',
            'annualHotDaysPerc' : u'No. of Days', #when Max Temp >'+str(cnst.HOTDAYS_THRESHOLD)+'$^{\circ}$C',
            'annualRainyDays' : u'No. of Rainy Days', # (>'+str(cnst.RAINYDAY_THRESHOLD)+'mm day$^{-1}$)',
            'annualRainyDaysPerc' : u'No. of Rainy Days', # (>'+str(cnst.RAINYDAY_THRESHOLD)+'mm day$^{-1}$)',
            'annualHotDays' : u'No. of Days', # when Max Temp >'+str(cnst.HOTDAYS_THRESHOLD)+'$^{\circ}$C',
            'annualExtremeRain30' : u'No. of Days', # > 30mm day$^{-1}$',
            'annualExtremeRain50' : u'No. of Days', # > 50mm day$^{-1}$',
            'annualExtremeRain100' : u'No. of Days', # > 100mm day$^{-1}$',
            'annualStrongWindDays' : u'No. of Days', # >'+str(cnst.STRONGWIND_THRESHOLD)+'ms$^{-1}$',
            'wetSpell10': u'No. of Wet Periods', # > 10 Days',
            'drySpell6': u'No. of Dry Periods', # > 6 Days',
            'annualMaxRain5dSum': u'5-day Total Precipitation',
            'annualMaxRain3dSum' : u'3-day Total Precipitation',
            'annualMaxRain2dSum' : u'2-day Total Precipitation',
            'annualMaxRain5dMean': u'5-day Mean Precipitation Rate (mm day$^{-1}$)',
            'annualMaxRain3dMean': u'3-day Mean Precipitation Rate (mm day$^{-1}$)',
            'annualMaxRain2dMean': u'2-day Mean Precipitation Rate (mm day$^{-1}$)',
            'SPIxMonthly' : u'SPI',
            'SPIbiannual' : u'SPI (bi-annual)',
            'onsetMarteau' : u'Julian Day',
            'cdd' : u'Consecutive Dry Days',
            'pet' : u'PET (mm day$^{-1}$)'
            },
            'FRANCAIS' : {
            'annualTotalRain' : u'Précipitations (mm)',
            'annualMeanRainyDay' : u'Précipitations (mm)',
            'annualHotDaysPerc' : u'Nb. de jours', #when Max Temp >'+str(cnst.HOTDAYS_THRESHOLD)+'$^{\circ}$C',
            'annualRainyDays' : u'Nb. de jours pluvieux', # (>'+str(cnst.RAINYDAY_THRESHOLD)+'mm day$^{-1}$)',
            'annualRainyDaysPerc' : u'Nb. de jours pluvieux', # (>'+str(cnst.RAINYDAY_THRESHOLD)+'mm day$^{-1}$)',
            'annualHotDays' : u'Nb. de jours', # when Max Temp >'+str(cnst.HOTDAYS_THRESHOLD)+'$^{\circ}$C',
            'annualExtremeRain30' : u'Nb. de jours', # > 30mm day$^{-1}$',
            'annualExtremeRain50' : u'Nb. de jours', # > 50mm day$^{-1}$',
            'annualExtremeRain100' : u'Nb. de jours', # > 100mm day$^{-1}$',
            'annualStrongWindDays' : u'Nb. de jours', # >'+str(cnst.STRONGWIND_THRESHOLD)+'ms$^{-1}$',
            'wetSpell10': u'Nb. de périodes pluvieuses', # > 10 Days',
            'drySpell6': u'Nb. de périodes sèches', # > 6 Days',
            'annualMaxRain5dSum': u'Précip. sur 5 jours',
            'annualMaxRain3dSum' : u'Précip. sur 3 jours',
            'annualMaxRain2dSum' : u'Précip. sur 2 jours',
            'annualMaxRain5dMean': u'Précipitations moyennes (depuis 5 jours ; mm jour$^{-1}$)',
            'annualMaxRain3dMean': u'Précipitations moyennes (depuis 3 jours ; mm jour$^{-1}$)',
            'annualMaxRain2dMean': u'Précipitations moyennes (depuis 2 jours ; mm jour$^{-1}$)',
            'SPIxMonthly' : u'SPI',
            'SPIbiannual' : u'SPI (bi-annuelle)',
            'onsetMarteau' : u'Jour julien',
            'cdd' : u'Nb. de jours secs consécutifs',
            'pet' : u'Evap. potentielle (mm jour$^{-1}$)'
            }
            }
    
    try:
        #if any([m in mykey for mykey in ylabLUT_metvar[cnst.LANGUAGE].keys()]):
        ylab = ylabLUT_metvar[cnst.LANGUAGE][metvar]
    except:
        ylab = ylabLUT[cnst.LANGUAGE][m]
    # ylab = cnst.VARNAMES[cnst.LANGUAGE][v] + ': ' + m

    unit = getUnit(v)
    if 'No.' in ylab:
        unit = u'(No.)'
    if 'Nb.' in ylab:
        unit = u'(Nb.)'
    
    if anom in ['percentage', 'percentageAnomaly']:
        ylab = u'% change ' if cnst.LANGUAGE == 'ENGLISH' else u'Changement (%)'
    if anom in ['absolute', 'anomaly']:
        ylab = u'Change '+unit if cnst.LANGUAGE == 'ENGLISH' else u'Changement '+unit
    
    return(ylab)

def getFigSize(region, plottype):
    
    if region:
        comb = plottype + '_' + region
    else:
        comb = plottype
    
    # (width, height)
    thisLUT = {'map_BF':(8,8),
               'map_SG': (8,8),
               'map_SH': (10,6),
               'map_SD': (10,6),
               'map_GC': (10,6),
               'nbModelHistogram': (8.5,6)
            }
    
    try:
        return(thisLUT[comb])
    except:
        return((9,9))
