'''
Contains functions to create labels in all types of plots
'''
import constants as cnst

DC = '$^\circ$C'

METRICLONGNAME = {
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
            'annualStrongWindDays' : 'Number of Days with Mean Wind Speed > '+str(cnst.STRONGWIND_THRESHOLD),
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
    }

MONTHS = [  'jan', 'feb', 'mar', 'apr','may', 'jun', 'jul', 'aug', 'sep','oct', 'nov','dec']


def getTitle(m, v, seas, scen, bc, r, anom=None):
    
    metvar = m + '_' + v
    
    if type(scen) == list:
        scen = ''
    else:
        scen = scen + '; '
    
    if anom in ['percentage', 'percentageAnomaly']:
        atxt = '% change in '
    elif anom in ['absolute', 'anomaly']:
        atxt = 'Change in '
    elif anom in ['scenarios']:
        # This covers the case for multi-scenario boxplots, and possibly others
        scen = ''
        atxt = ''
    else:
        atxt = ''

    # e.g. Burkina Faso: Number of days when daily maximum temperature exceeds 40C (JAS)
    titleLUT = {
            'annualMax_pr' : r + ': ' + atxt + METRICLONGNAME[m] + ' ' + cnst.VARNAMES[v].title() + '\n('+seas+'; '+scen+bc+')',
            'annualMax_tasmax' : r + ': ' + atxt + METRICLONGNAME[m] + ' ' + cnst.VARNAMES[v].title() + '\n('+seas+'; '+scen+bc+')',
            'annualMax_rsds' : r + ': ' + atxt + METRICLONGNAME[m] + ' ' + cnst.VARNAMES[v].title() + '\n('+seas+'; '+scen+bc+')',
            'annualMin_tasmin' : r + ': ' + atxt + METRICLONGNAME[m] + ' ' + cnst.VARNAMES[v].title() + '\n('+seas+'; '+scen+bc+')',
            'annualMean_tas' : r + ': ' + atxt + METRICLONGNAME[m] + ' ' + cnst.VARNAMES[v].title() + '\n('+seas+'; '+scen+bc+')',
            'annualMean_rsds' : r + ': ' + atxt + METRICLONGNAME[m] + ' ' + cnst.VARNAMES[v].title() + '\n('+seas+'; '+scen+bc+')',
            'monthlyClimatologicalMean_pr' : r + ': ' + atxt + METRICLONGNAME[m] + ' ' + cnst.VARNAMES[v].title() + '\n('+seas+'; '+scen+bc+')',
            'monthlyClimatologicalMean_tasmin' : r + ': ' + atxt + METRICLONGNAME[m] + ' ' + cnst.VARNAMES[v].title() + '\n('+seas+'; '+scen+bc+')',
            'monthlyClimatologicalMean_tas' : r + ': ' + atxt + METRICLONGNAME[m] + ' ' + cnst.VARNAMES[v].title() + '\n('+seas+'; '+scen+bc+')',
            'monthlyClimatologicalMean_tasmax' : r + ': ' + atxt + METRICLONGNAME[m] + ' ' + cnst.VARNAMES[v].title() + '\n('+seas+'; '+scen+bc+')',
            'monthlyClimatologicalMean_rsds' : r + ': ' + atxt + METRICLONGNAME[m] + ' ' + cnst.VARNAMES[v].title() + '\n('+seas+'; '+scen+bc+')',
            'monthlyClimatologicalMean_wind' : r + ': ' + atxt + METRICLONGNAME[m] + ' ' + cnst.VARNAMES[v].title() + '\n('+seas+'; '+scen+bc+')'
            }
    
    try:
        return(titleLUT[metvar])
    except:
        temp_title = r + ': ' + atxt + METRICLONGNAME[m] + '\n('+seas+'; '+scen+bc+')'
        return(temp_title)

def getUnit(var):

    vardic = {
        'pr': '(mm day$^{-1}$)',
        'tasmax': '('+DC+')' ,
        'rsds': '(W m$^{-2}$)',
        'tasmin': '(' + DC + ')',
        'tas': '(' + DC + ')',
        'wind': '(m s$^{-1}$)'
    }

    return vardic[var]


def getYlab(m, v, anom=None):
    
    metvar = m + '_' + v
    
    ylabLUT_metvar = {
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
    
    ylabLUT = {
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
            }
    
    try:
        if any([m in mykey for mykey in ylabLUT_metvar.keys()]):
            ylab = ylabLUT_metvar[metvar]
        else:
            ylab = ylabLUT[m]
    except:
        ylab = cnst.VARNAMES[v] + ': ' + m

    unit = getUnit(v)
    
    if anom in ['percentage', 'percentageAnomaly']:
        ylab = '% change '#in ' + ylab
    if anom in ['absolute', 'anomaly']:
        ylab = 'Absolute change '+unit# in ' + ylab
    
    return(ylab)

def getFigSize(region, plottype):
    
    if region:
        comb = plottype + '_' + region
    else:
        comb = plottype
    
    # (width, height)
    thisLUT = {'map_BF': (7,7),
               'map_SG': (6,8),
               'map_WA': (8,6),
               'nbModelHistogram': (8.5,6)
            }
    
    try:
        return(thisLUT[comb])
    except:
        return((9,9))