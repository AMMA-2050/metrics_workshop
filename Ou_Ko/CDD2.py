import os
import matplotlib.pyplot as plt
import numpy as np
import iris
import iris.quickplot as qplt

wet = np.zeros(12)
def plotCWD(infile, figcwd):
   
   """
   
    This script will calculate and plot a consecutive dry days over West Africa Guinea Coast
    
   """ 

def calcDryDays(incube, outpath):
    '''
    Inputs
        - incube : must have time dimension with year, month_number and season, and units in kg m-2 day-1
    Outputs
        - ?
    '''
    
    try:
        mdrydays=iris.load_cube(outpath+'meandrydays_permonth.nc')

    except IOError:
    
        print 'Calculating Number of Dry Days per Month'
        print incube
        drydays = incube.aggregated_by(['year','month_number'], iris.analysis.COUNT, function = lambda values: values <= 1.0 )
        print drydays
        
        mdrydays = drydays.aggregated_by('month_number', iris.analysis.MEAN)
        iris.save(mdrydays,outpath+'meandrydays_permonth.nc')
    
    return(mdrydays)
    
def main():
    
    outpath = '/nfs/a266/earv054/'
    # this is the function that controls everything 
    mycube = iris.load_cube('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/MIROC5/historical/pr_WFDEI_1979-2013_0.5x0.5_day_MIROC5_africa_historical_r1i1p1_full.nc')
    #print my_cube
    mycube_wafr = mycube.intersection(latitude=(2.0, 12.0), longitude=(-20.0, 20.0))
    iris.coord_categorisation.add_year(mycube_wafr, 'time',name='year')
    iris.coord_categorisation.add_season(mycube_wafr, 'time',name='season')
    iris.coord_categorisation.add_month_number(mycube_wafr, 'time',name='month_number')
    mycube_wafr.convert_units('kg m-2 day-1')
    
    mdrydays = calcDryDays(mycube_wafr, outpath)
    
if __name__ == '__main__': 
    main() 
        
        
        
        
