import os, sys
from glob import glob
from operator import itemgetter
import subprocess
import constants as cnst

'''
This script loops through all images created by the atlas plotting script, 
and writes them into a LaTex file for writing the atlas pdf.

By   : Andy Hartley
Email: andrew.hartley@metoffice.gov.uk
Date : 2nd May 2017
'''

def getIntroText(metric):
    
    intro_text = {
        'SPI_xmonthly' : 'The Standardised Precipitation Index (SPI) is a metric which was developed primarily for defining and monitoring drought. It allows a user to determine the rarity of drought at a given time scale of interest. It can also be used to determine periods of anomalously wet events.',
        'Marteau_onset': 'Local Agronomic Monsoon Onset Date (Marteau) is defined as the first rainy day (precipitation greater than 1 mm) of two consecutive rainy days (with total precipitation greater than 20 mm) and no 7-day dry spell with less than 5 mm of rainfall during the subsequent 20 days',
        'Fitzpatrick_onset' : 'Local Agronomic Monsoon Onset Date (Fitzpatrick)',
        'annual_max'   : 'Annual Maximum Precipitation',
        'numberdays30mm' : 'Number of days where precipitation is greater than 30mm in the aggregation period',
        'total_rain'   : 'Total amount of precipitation during the aggregation period'
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
    
    
def getMetricNiceName(name):
    
    full_name = {
        'SPI_xmonthly' : 'Standardised Precipitation Index',
        'Marteau_onset': 'Local Agronomic Monsoon Onset Date (Marteau)',
        'Fitzpatrick_onset' : 'Local Agronomic Monsoon Onset Date (Fitzpatrick)',
        'annual_max' : 'Annual Maximum Precipitation',
        'numberdays30mm' : 'Number of days where precipitation is greater than 30mm',
        'total_rain'   : 'Total amount of precipitation during the aggregation period'
    }
    return(full_name[name])
    
def getNicePlotName(plot_name):
    
    nice_plot_name = {
        'Sahel_10th_90th_percentile' : 'The 90th (a) and 10th (b) percentile changes from the CMIP5 ensemble',
        'Sahel_all_model_boxplot'    : 'Box plots of range across the CMIP5 ensemble for the Sahel',
        'Sahel_all_model_histogram'  : 'The histograms show xxx for each CMIP5 ensemble member',
        'Sahel_all_model_perc_scatter_difference' : 'Ordered scatterplot'
    }
    try:
        return(nice_plot_name[plot_name])
    except:
        sys.exit('Unable to find ' + plot_name + 'in the function \'getNicePlotName\'')

def getFullCaption(metric, bc, rcp, seas, plotnm):
    
    start = {
        'Sahel_10th_90th_percentile' : 'These maps show ',
        'Sahel_all_model_perc_scatter_difference' : 'This scatterplot shows ',
        'Sahel_all_model_boxplot' : 'Boxplots showing ',
        'Sahel_all_model_histogram' : 'Bar plot showing '
    }
    
    metric_desc = {
        'Marteau_onset' : 'the date of monsoon onset as defined by Marteau et al. (2009) for the season '+monthLookUp(seas)+' in the 2050s (2040 to 2069). ',
        'SPI_xmonthly'  : 'the Standardised Precipitation Index for the season '+monthLookUp(seas)+' in the 2050s (2040 to 2069). ',
        'Fitzpatrick_onset' : 'the date of monsoon onset as defined by Fitzpatrick et al. (2016) for the season '+monthLookUp(seas)+' in the 2050s (2040 to 2069). ',
        'annual_max'    : 'annual maximum precipitation',
        'numberdays30mm' : 'the number of days where precipitation is greater than 30mm for the season '+monthLookUp(seas)+' in the 2050s (2040 to 2069). ',
        'total_rain'   : 'Total amount of precipitation for the season '+monthLookUp(seas)+' in the 2050s (2040 to 2069). '
    }
    
    statistic_desc = {
        'Sahel_10th_90th_percentile' : 'The 90th (a) and 10th (b) percentile changes from the CMIP5 ensemble are shown for '+rcp+' compared to the historical period (1950-2000).',
        'Sahel_all_model_boxplot'    : 'The boxes show the interquartile range across the CMIP5 ensemble, dotted lines the 10th to 90th percentile range, and red line the ensemble median.',
        'Sahel_all_model_histogram'  : 'The histograms show xxx for each CMIP5 ensemble member',
        'Sahel_all_model_perc_scatter_difference' : 'The scatterplot shows each ensemble member ordered according to xxx'
    }
    
    mycaption = start[plotnm] + metric_desc[metric] + statistic_desc[plotnm]
    return(mycaption)
    

def getShortCaption(metric, bc, rcp, seas, plotnm):
    
    mycaption = 'As above, but for ' + monthLookUp(seas) + ' for ' + rcp + ' in the 2050s compared to historical (1950-2000). The bias corrected dataset used was ' + bc.replace("_", "\_") + '.'
    return(mycaption)

# def writeTex(ofile):
#     with open(ofile,"w") as fout:
#         fout.write(line+"\r\n")
#         \documentclass[11pt, oneside]{article}
# \usepackage{geometry}                		% See geometry.pdf to learn the layout options. There are lots.
# \geometry{letterpaper}                   		% ... or a4paper or a5paper or ... 
# \usepackage{graphicx}				% Use pdf, png, jpg, or eps§ with pdflatex; use eps in DVI mode
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


def main():
    version = "v0.2.2"
    texdir = cnst.METRIC_ATLASDIR # os.getcwd()  
    imgdir = cnst.METRIC_PLOTDIR # texdir + '/images/'
    imgfiles = sorted(glob(imgdir + '*.png'))
    
    metric_names = [os.path.basename(f).split('-')[0] for f in imgfiles]
    plot_sections = []
    last_plot_name = []
    last_metric = []
    section_counter = 2 # Starts at 2 because 1 is the Introduction
    
    # Loop through a sorted list of metric_names
    for metric in sorted(set(metric_names)):
        print(metric)
        # Which imgfiles have this metric name?
        i_imgs = [y for y,x in enumerate(metric_names) if x == metric]
        
        metric_tuple = [(os.path.basename(imgfiles[i]).split('-')[4].rstrip('.png'), 
        os.path.basename(imgfiles[i]).split('-')[1], 
        os.path.basename(imgfiles[i]).split('-')[2], 
        os.path.basename(imgfiles[i]).split('-')[3]) for i in i_imgs]
        
        # Create a new section for this metric
        section_fname = texdir + '/' + str(section_counter) + "_" + metric + ".tex"
        if os.path.isfile(section_fname):
            print(section_fname)
            os.remove(section_fname)
                
        fmetric = open(section_fname, "w+")
        fmetric.write('\section{'+getMetricNiceName(metric)+'} \label{sec:'+metric+'}\r\n')
        fmetric.write('\r\n')
        
        # Write some introductory text
        fmetric.write(getIntroText(metric) + '\r\n')
        fmetric.write('\r\n')
        
        # Loop through all plots for this metric
        # NB: Sorting alphabetically by:
        #       1. Plot name
        #       2. Season
        #       3. historical/rcp
        #       4. Bias correction method
        for plot_name, bc_name, scen_name, seas_name in sorted(metric_tuple, key=itemgetter(0,3,2,1)):
            
            this_file = "images/" + '-'.join([metric, bc_name, scen_name, seas_name, plot_name]) + ".png"
            # Create a subsection for this plot type
            
            if last_plot_name != plot_name or last_metric != metric:
                fmetric.write('\subsection{'+getNicePlotName(plot_name)+'}\r\n')
                fmetric.write('\r\n')
            
            # Write the image into the tex file for this section
            fmetric.write('\\begin{figure}[!htb]\r\n')
            fmetric.write('\\begin{center}\r\n')
            fmetric.write('\\includegraphics[width=\\textwidth]{'+this_file+'}\r\n')
            fmetric.write('\\end{center}\r\n')
            
            if last_plot_name == plot_name:
                fmetric.write('\\caption{'+getShortCaption(metric, bc_name, scen_name, seas_name, plot_name)+'}\r\n')
            else:
                fmetric.write('\\caption{'+getFullCaption(metric, bc_name, scen_name, seas_name, plot_name)+'}\r\n')
            
            fmetric.write('\\label{fig:'+os.path.basename(this_file).rstrip(".png")+'}\r\n')
            fmetric.write('\\end{figure}\r\n')
            fmetric.write('\r\n')
            
            last_plot_name = plot_name
            last_metric    = metric
        
        fmetric.close()
        plot_sections.append(str(section_counter) + "_" + metric)
        
        # print(section_counter)
        section_counter += 1

    # At the end, write the section names into atlas.tex
    # writeTex("atlas_"+version+".tex")
    # print(plot_sections)
    with open("atlas_template.tex", "r") as fin, open("atlas_"+version+".tex","w") as fout:
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
    subprocess.call(["pdflatex", "atlas_"+version+".tex"])
    subprocess.call(["pdflatex", "atlas_"+version+".tex"])
    
    print('File successfully created: ' + texdir + "/atlas_" +version+ ".pdf")
    
if __name__ == "__main__":
    main()
    