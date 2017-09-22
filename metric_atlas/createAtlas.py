import os
from glob import glob
from operator import itemgetter
import subprocess
import constants as cnst
import labeller as lblr
import itertools
import utils
import pdb

'''
This script loops through all images created by the atlas plotting script, 
and writes them into a LaTex file for writing the atlas pdf.

By   : Andy Hartley
Email: andrew.hartley@metoffice.gov.uk
Date : 2nd May 2017
'''

def getIntroText(metric):
    
    intro_text = {
            'annualMax' : 'This shows the maximum daily value for each variable, for the period shown.',
            'annualMin' : 'This shows the minimum daily value for each variable, for the period shown.',
            'annualTotalRain' : 'This shows the total accumulated rainfall for the period shown.',
            'annualMean' : 'This shows the mean daily value for each variable, for the period shown.',
            'annualMeanRainyDay' : 'This shows the mean rainfall on the days that it rained with the period shown.',
            'monthlyClimatologicalMean' : 'This shows the climatology for each variable for each month within the period shown.',
            'annualRainyDays' : 'This shows the number of days per in the period shown when rainfall was above a threshold of '+str(cnst.RAINYDAY_THRESHOLD)+'mm/day.',
            'annualRainyDaysPerc' : 'This shows the percentage of days in the period shown when rainfall was above a threshold of '+str(cnst.RAINYDAY_THRESHOLD)+'mm/day.',
            'annualHotDays' : 'This shows the number of days in the period shown with a Daily Maximum Temperature exceeding '+str(cnst.HOTDAYS_THRESHOLD)+lblr.DC+'.',
            'annualExtremeRain30' : 'This shows the number of days in the period shown when rainfall exceeds a threshold of 30mm/day',
            'annualExtremeRain50' : 'This shows the number of days in the period shown when rainfall exceeds a threshold of 50mm/day',
            'annualExtremeRain100' : 'This shows the number of days in the period shown when rainfall exceeds a threshold of 100mm/day',
            'annualStrongWindDays' : 'This shows the number of days in the period shown when daily mean wind speed exceeds a threshold of '+str(cnst.STRONGWIND_THRESHOLD)+'m/s',
            'wetSpell10': 'This shows the number of periods with a wet spell longer than 10 days for the season shown.',
            'drySpell6': 'This shows the number of periods with a dry spell longer than 6 days for the season shown.',
            'annualMaxRain5dSum': 'Annual Maximum Rainfall Total in a 5-day Period',
            'annualMaxRain3dSum' : 'Annual Maximum Rainfall Total in a 3-day Period',
            'annualMaxRain2dSum' : 'Annual Maximum Rainfall Total in a 2-day Period',
            'annualMaxRain5dMean': 'Annual Maximum Rainfall in a 5-day Period (Mean Daily Rate)',
            'annualMaxRain3dMean': 'Annual Maximum Rainfall in a 3-day Period (Mean Daily Rate)',
            'annualMaxRain2dMean': 'Annual Maximum Rainfall in a 2-day Period (Mean Daily Rate)',
            'SPIxMonthly' : 'The Standardised Precipitation Index (SPI) is a metric which was developed primarily for defining and monitoring drought. It allows a user to determine the rarity of drought at a given time scale of interest. It can also be used to determine periods of anomalously wet events.',
            'SPIbiannual' : 'The Standardised Precipitation Index (SPI) is a metric which was developed primarily for defining and monitoring drought. It allows a user to determine the rarity of drought at a given time scale of interest. It can also be used to determine periods of anomalously wet events. In this case, a 2-year rolling window is used.',
            'onsetMarteau' : 'Local Agronomic Monsoon Onset Date (Marteau) is defined as the first rainy day (precipitation greater than 1 mm) of two consecutive rainy days (with total precipitation greater than 20 mm) and no 7-day dry spell with less than 5 mm of rainfall during the subsequent 20 days',
            'cdd' : 'Consecutive Dry Days'
            }
    
    return(intro_text[metric])
    
def monthLookUp(abrv):
    
    month_long_names = {
        'mjjas' : 'May to September',
        'amj'   : 'April, May and June',
        'jas'   : 'July, August and September',
        'ond'   : 'October, November and December',
        'mj'    : 'May and June',
        'jj'    : 'June and July',
        'ja'    : 'July and August',
        'as'    : 'August and September',
        'so'    : 'September and October',
        'ann'   : 'Annual'
    }
    
    return(month_long_names[abrv])
    
    
def getMetricNiceName(name, var):
    
    if name in ['annualMax', 'annualMin', 'annualMean', 'monthlyClimatologicalMean']:
        oname = lblr.METRICLONGNAME[name] + cnst.VARNAMES[var].title()
    else:
        oname = lblr.METRICLONGNAME[name]
        
    return(oname)
    
def getNicePlotName(plot_name):
    
    nice_plot_name = {
            'allModelRank' : 'Model ranking scatterplots', 
            'mapPerc' : 'Maps of ensemble spread (10th and 90th percentiles)',
            'nbModelHistogram' : '\'Number of model\' histograms', 
            'MultiNbModelHistogram' : '\'Number of model\' histograms for all scenarios', 
            'allModelBoxplot' : 'Boxplots', 
            'lineplot' : 'Spaghetti timeseries', 
            'allModelHisto' : '\'All Model\' histograms'
    }
    try:
        return(nice_plot_name[plot_name])
    except:
        return(plot_name)
#        sys.exit('Unable to find ' + plot_name + 'in the function \'getNicePlotName\'')

def getNicePlotType(plot_type):
    nice_plottype_name ={
            'rcp26PercentageAnomaly' : '% Anomaly by Scenario', 
            'rcp5PercentageAnomaly' : '% Anomaly by Scenario', 
            'rcp85PercentageAnomaly' : '% Anomaly by Scenario', 
            'rcp26Anomaly' : 'Absolute Anomaly by Scenario', 
            'rcp45Anomaly' : 'Absolute Anomaly by Scenario', 
            'rcp85Anomaly' : 'Absolute Anomaly by Scenario', 
            'rcp26' : 'Each Scenario', 
            'rcp45' : 'Each Scenario', 
            'rcp85' : 'Each Scenario', 
            'scenarios' : 'All scenarios', 
            'historical' : 'Each Scenario', 
            'percentageAnomaly' : 'Percentage Anomaly', 
            'anomaly' : 'Absolute Anomaly', 
            'allscen' : 'All scenarios for 1950-2100'
            }
    try:
        return(nice_plottype_name[plot_type])
    except:
        return(plot_type)


def getFullCaption(metric, bc, seas, plotnm):
    
    start = {
            'allModelRank' : 'This scatterplot shows ', 
            'mapPerc' : 'These maps show ',
            'nbModelHistogram' : 'Histograms showing ', 
            'MultiNbModelHistogram' : 'Histograms showing ', 
            'allModelBoxplot' : 'Boxplots showing', 
            'lineplot' : 'Timeseries plots showing ', 
            'allModelHisto' : 'Histograms showing '
    }
    
    metric_desc = {
        'annualMax' : 'Annual Maximum',
        'annualMin' : 'Annual Minimum',
        'annualTotalRain' : 'Total Annual Rainfall',
        'annualMean' : 'Annual Mean',
        'annualMeanRainyDay' : 'Mean Daily Rainfall on Rainy Days',
        'monthlyClimatologicalMean' : 'Monthly Climatological Mean',
        'annualHotDaysPerc' : 'Percentage of Hot Days (Daily Max Temp >'+str(cnst.HOTDAYS_THRESHOLD)+lblr.DC+' per Year',
        'annualRainyDays' : 'Number of Rainy Days (>'+str(cnst.RAINYDAY_THRESHOLD)+'mm/day) per Year',
        'annualRainyDaysPerc' : 'Percentage of Days that are Rainy (>'+str(cnst.RAINYDAY_THRESHOLD)+'mm/day) per Year',
        'annualHotDays' : 'Number of Days per Year with a Daily Maximum Temperature exceeding '+str(cnst.HOTDAYS_THRESHOLD)+lblr.DC+' per Year',
        #            'annualExtremeRain30' : 'Number of Days per Year when Rainfall Exceeds 30mm/day',
        #            'annualExtremeRain50' : 'Number of Days per Year when Rainfall Exceeds 50mm/day',
        #            'annualExtremeRain100' : 'Number of Days per Year when Rainfall Exceeds 100mm/day',
        'annualStrongWindDays' : 'Number of Days per Year when Daily Mean Wind Speed Exceeds '+str(cnst.STRONGWIND_THRESHOLD),
        'wetSpell10': 'Number of Periods with a Wet Spell Longer Than 10 Days',
        'drySpell6': 'Number of Periods with a Dry Spell Longer Than 6 Days',
        'annualMaxRain5dSum': 'Annual Maximum Rainfall Total in a 5-day Period',
        'annualMaxRain3dSum' : 'Annual Maximum Rainfall Total in a 3-day Period',
        'annualMaxRain2dSum' : 'Annual Maximum Rainfall Total in a 2-day Period',
        'annualMaxRain5dMean': 'Annual Maximum Rainfall in a 5-day Period (Mean Daily Rate)',
        'annualMaxRain3dMean': 'Annual Maximum Rainfall in a 3-day Period (Mean Daily Rate)',
        'annualMaxRain2dMean': 'Annual Maximum Rainfall in a 2-day Period (Mean Daily Rate)',
        'cdd' : 'Consecutive Dry Days',
        'onsetMarteau' : 'the date of monsoon onset as defined by Marteau et al. (2009) for the season '+monthLookUp(seas)+' in the 2050s (2040 to 2069). ',
        'SPIxmonthly'  : 'the Standardised Precipitation Index for the season '+monthLookUp(seas)+' in the 2050s (2040 to 2069). ',
        'SPIbiannual' : 'the bi-annual Standardised Precipitation Index for the season '+monthLookUp(seas)+' in the 2050s (2040 to 2069). ',
        'Fitzpatrick_onset' : 'the date of monsoon onset as defined by Fitzpatrick et al. (2016) for the season '+monthLookUp(seas)+' in the 2050s (2040 to 2069). ',
        #'annualMax'    : 'annual maximum precipitation',
        'annualExtremeRain30' : 'the number of days when rainfall exceeds 30mm/day for the season '+monthLookUp(seas)+' in the 2050s ('+str(cnst.FUTURE[0])+' to '+str(cnst.FUTURE[0])+'). ',
        'annualExtremeRain50' : 'the number of days when rainfall exceeds 50mm/day for the season '+monthLookUp(seas)+' in the 2050s ('+str(cnst.FUTURE[0])+' to '+str(cnst.FUTURE[0])+'). ',
        'annualExtremeRain100' : 'the number of days when rainfall exceeds 100mm/day for the season '+monthLookUp(seas)+' in the 2050s ('+str(cnst.FUTURE[0])+' to '+str(cnst.FUTURE[0])+'). ',
        'total_rain'   : 'Total amount of precipitation for the season '+monthLookUp(seas)+' in the 2050s (2040 to 2069). '
    }
    
    statistic_desc = {
            'allModelRank' : 'The scatterplot shows each ensemble member ordered according to xxx.', 
            'mapPerc' : 'The 90th (a) and 10th (b) percentile changes from the CMIP5 ensemble are shown for rcp scenarios compared to the historical period (1950-2000).',
            'nbModelHistogram' : 'The histograms show how many models agree on the same magnitude of the variable shown.', 
            'MultiNbModelHistogram' : 'The histograms show how many models agree on the same magnitude of the variable shown.', 
            'allModelBoxplot' : 'The boxes show the interquartile range (black lines) across the CMIP5 ensemble, dotted lines the 10th to 90th percentile range, and small green lines show each model.', 
            'lineplot' : 'Each line represents a different CMIP5 ensemble model.', 
            'allModelHisto' : 'The histograms show xxx for each CMIP5 ensemble member.'            
    }
    
    mycaption = start[plotnm] + metric_desc[metric] + statistic_desc[plotnm]
    return(mycaption)
    

def getShortCaption(metric, bc, seas, plotnm):
    
    mycaption = 'As above, but for ' + monthLookUp(seas) + ' in the 2050s (2040-2069) compared to historical (1950-2000). The bias corrected dataset used was ' + bc.replace("_", "\_") + '.'
    return(mycaption)

# def writeTex(ofile):
#     with open(ofile,"w") as fout:
#         fout.write(line+"\r\n")
#         \documentclass[11pt, oneside]{article}
# \usepackage{geometry}                		% See geometry.pdf to learn the layout options. There are lots.
# \geometry{letterpaper}                   		% ... or a4paper or a5paper or ... 
# \usepackage{graphicx}				% Use pdf, png, jpg, or eps with pdflatex; use eps in DVI mode
# \usepackage{grffile}                                   % Searches for welknown image extensions. graphicx uses the first dot it finds ... which doesn't help when we have long filenames with dots in
# \usepackage{amssymb}
# \usepackage{setspace,caption}
# \usepackage[titletoc,title]{appendix}
# \usepackage[linkcolor=blue,colorlinks=true,urlcolor=blue,citecolor=black]{hyperref}

        
#         for line in fin.readline():
#             print(line)
#             if line == '%InsertHere':
#                 print('\section{'+getMetricNiceName(metric)+'}')
#                 # fout.write('\section{'+getMetricNiceName(metric)+'}')
#             else:
#                 # fout.write(line+"\r\n")
#                 print(line)


def runAtlas():
    version = cnst.VERSION
    texdir = cnst.METRIC_ATLASDIR # os.getcwd()  
    imgdir = cnst.METRIC_PLOTDIR # texdir + '/images/'
    
    if not os.path.isdir(texdir):
        os.makedirs(texdir)
    
    plot_sections = []
#    last_plot_name = []
#    last_metric = []
    section_counter = 2 # Starts at 2 because 1 is the Introduction
    
    # Metric-specific options are set in constants.py
    for row in cnst.METRICS_TORUN:
        
        metric = row[0]
        variable = row[1] # NB: Could be multiple
        season = row[2] # NB: Could be multiple
        
        for var in variable:
            # Create a new section for this metric
            section_fname = texdir + '/' + str(section_counter) + "_" + metric + "_" + var + ".tex"
            print section_fname
            if os.path.isfile(section_fname):
                os.remove(section_fname)
                    
            fmetric = open(section_fname, "w+")
            fmetric.write('\section{'+getMetricNiceName(metric, var)+'} \label{sec:'+metric+'}\r\n')
            fmetric.write('\r\n')
            
            # Write some introductory text
            fmetric.write(getIntroText(metric) + '\r\n')
            fmetric.write('\r\n')
        
            for seas, region, bc_res in itertools.product(season, cnst.REGIONS_LIST, cnst.BC_RES):
                reg = region[0]
                imgfiles = sorted(glob(imgdir + os.sep + bc_res + os.sep + metric + os.sep + metric + '_' + var + '_' + bc_res + seas +'_'+reg+ '*.png'))
                
                imgdata = [utils.split_imgname(imgfile) for imgfile in imgfiles]
                
                plotnames = list(set([id['plotname'] for id in imgdata]))
                plottypes = list(set([id['plottype'] for id in imgdata]))
                
                
                # Loop through all plotnames associated with this metric-var combination
                for pn in plotnames:
                    
                    # Make sub section
                    # Create a subsection for this plot name
#                    if last_plot_name != pn or last_metric != metric:
                    fmetric.write('\subsection{'+getNicePlotName(pn)+'}\r\n')
                    fmetric.write('\r\n')

                    
                    for pt in plottypes:
                        
                        # Create a subsection for this plot name
#                        if last_plot_type != pt or last_metric != metric:
                        fmetric.write('\subsubsection{'+getNicePlotType(pt)+'}\r\n')
                        fmetric.write('\r\n')
                        
                        # Now, get all filename associated with this metric-var-(seas/reg/bc_res)-plotname-plottype
                        pdb.set_trace()
                        
                        # Make Sub-sub section
                        # NB: plottype also contains the scenario information
                        this_file = imgdir + os.sep + bc_res + os.sep + metric + os.sep + '_'.join([metric, var, bc_res, seas, reg, pn, pt]) + ".png"
                            
                        # Write the image into the tex file for this section
                        fmetric.write('\\begin{figure}[!htb]\r\n')
                        fmetric.write('\\begin{center}\r\n')
                        fmetric.write('\\includegraphics[width=\\textwidth]{'+this_file+'}\r\n')
                        fmetric.write('\\end{center}\r\n')
                        
#                        if last_plot_name == pn:
#                            fmetric.write('\\caption{'+getShortCaption(metric, bc_res, seas, pt)+'}\r\n')
#                        else:
#                            fmetric.write('\\caption{'+getFullCaption(metric, bc_res, seas, pt)+'}\r\n')
                        fmetric.write('\\caption{'+getFullCaption(metric, bc_res, seas, pt)+'}\r\n')

                        fmetric.write('\\label{fig:'+os.path.basename(this_file).rstrip(".png")+'}\r\n')
                        fmetric.write('\\end{figure}\r\n')
                        fmetric.write('\r\n')

            #
            fmetric.close()
            plot_sections.append(texdir + "/" + str(section_counter) + "_" + metric + "_" + var)
            
            print(section_counter)
            section_counter += 1
            
    # At the end, write the section names into atlas.tex
    # writeTex("atlas_"+version+".tex")
    # print(plot_sections)
    with open("atlas_template.tex", "r") as fin, open(texdir + "/atlas_"+version+".tex","w") as fout:
        for line in fin:
            # print(line.encode("utf-8"))
            if line.strip() == '%InsertHere':
                for pltsec in plot_sections:
                    print('\include{'+pltsec+'}')
                    fout.write('\include{'+pltsec+'}\r\n')
                # fout.write('%InsertHere\r\n')
            else:
                fout.write(line+'\r\n')

    # Compile TWICE in latex
    subprocess.call(["pdflatex", texdir + "/" + "atlas_"+version+".tex"])
    subprocess.call(["pdflatex", texdir + "/" + "atlas_"+version+".tex"])
    
    print('File successfully created: ' + texdir + "/atlas_" +version+ ".pdf")
    