'''
Contains functions to create labels in all types of plots
'''
import constants as cnst

DC = u'\N{DEGREE SIGN}C'

METRICLONGNAME = {'annualHotDays': 'Number of Days Exceeding ' + \
               str(cnst.HOTDAYS_THRESHOLD) + u'\N{DEGREE SIGN}C',
               'annualHotDaysPerc': 'Percentage of Days Exceeding ' + \
               str(cnst.HOTDAYS_THRESHOLD) + u'\N{DEGREE SIGN}C', 
               'annualMax': 'Annual Maximum',
               'onsetMarteau': 'Date of Monsoon Onset (Marteau method)'
        }


def getTitle(m, v, seas, scen, bc, r, anom=None):
    
    metvar = m + '_' + v
    
    if type(scen) == list:
        scen = ''
    else:
        scen = scen + '; '
    
    if anom in ['percentage', 'percentageAnomaly']:
        atxt = '% Change in '
    elif anom in ['absolute', 'anomaly']:
        atxt = 'Change in '
    elif anom in ['scenarios']:
        # This covers the case for multi-scenario boxplots, and possibly others
        scen = ''
        atxt = ''
    else:
        atxt = ''

    # e.g. Burkina Faso: Number of days exceeding 40C (JAS)
    titleLUT = {'AnnualHotDays_tasmax': r + ': ' + atxt + METRICLONGNAME[m] + ' ' + cnst.VARNAMES[v].title() + '\n('+seas+'; '+scen+bc+')',
                'AnnualHotDaysPerc_tasmax': r + ': ' + atxt + METRICLONGNAME[m] + ' ' + cnst.VARNAMES[v].title() + '\n('+seas+'; '+scen+bc+')',
                'annualMax_pr': r + ': ' + atxt + METRICLONGNAME[m] + ' ' + cnst.VARNAMES[v].title() + '\n('+seas+'; '+scen+bc+')',
                'annualMax_tasmax': r + ': ' + atxt + METRICLONGNAME[m] + ' ' + cnst.VARNAMES[v].title() + '\n('+seas+'; '+scen+bc+')',
                'onsetMarteau_pr': r + ': ' + atxt + METRICLONGNAME[m] + '\n('+seas+'; '+scen+bc+')'
            }
    
    try:
        return(titleLUT[metvar])
    except:
        temp_title = r + ': ' + m + ', ' + v + ' ('+seas+'; '+scen+'; '+bc+')'
        return(temp_title)


def getYlab(m, v, anom=None):
    
    metvar = m + '_' + v
    
    ylabLUT = {'AnnualHotDays_tasmax': 'No. of Days >'+str(cnst.HOTDAYS_THRESHOLD) + DC,
               'AnnualHotDaysPerc_tasmax': '% of Days >'+str(cnst.HOTDAYS_THRESHOLD) + DC,
               'annualMax_pr': 'Daily Precipitation (mm/day)',
               'annualMax_tasmax': 'Daily Max Temperature ('+DC+')',
               'onsetMarteau_pr': 'Onset Day (Julian Day)'
            }
    
    try:
        ylab = ylabLUT[metvar]
    except:
        ylab = cnst.VARNAMES[v] + ': ' + m
    
    if anom in ['percentage', 'percentageAnomaly']:
        ylab = '% Change in ' + ylab
    if anom in ['absolute', 'anomaly']:
        ylab = 'Change in ' + ylab
    
    return(ylab)

def getFigSize(region, plottype):
    
    if region:
        comb = plottype + '_' + region
    else:
        comb = plottype
    
    # (width, height)
    thisLUT = {'map_BF': (7,8),
               'map_SG': (6,8),
               'map_WA': (8,6),
               'nbModelHistogram': (7,6)
            }
    
    try:
        return(thisLUT[comb])
    except:
        return((9,9))