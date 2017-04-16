#############################################################

#SCRIPT TO CALCULATE THE NUMBER OF WET DAYS (>1mm) PER YEAR

#############################################################

import itertools
import iris
import iris.coord_categorisation
    
def calcWetDays(incube, outpath):
    '''
    Inputs
        - incube : must have time dimension with year, month_number and season, and units in kg m-2 day-1
    Outputs
        - ?
    '''
    
    try:
        #mwetdays=iris.load_cube(outpath+'meanwetdays_permonth.nc')
        #swetdays=iris.load_cube(outpath+'meanwetdays_perseason.nc')
        ywetdays=iris.load_cube(outpath+'meanwetdays_peryear.nc')
    except IOError:
    
        print 'Calculating Number of Wet Days per Year'
        print incube
        wetdays = incube.aggregated_by(['year'], iris.analysis.COUNT, function = lambda values: values > 1.0 )
        print wetdays
        
        #mwetdays = wetdays.aggregated_by('month_number', iris.analysis.MEAN)
        #iris.save(mwetdays,outpath+'meanwetdays_permonth.nc')
        
        #swetdays = wetdays.aggregated_by('season_year', iris.analysis.MEAN)
        #iris.save(swetdays,outpath+'meanwetdays_perseason.nc')
        
        ywetdays = wetdays.aggregated_by('year', iris.analysis.MEAN)
        iris.save(ywetdays,outpath+'meanwetdays_peryear.nc')
    return(ywetdays)

def main():
    
    outpath = '/home/kobby/Desktop/'
    # this is the function that controls everything 
    mycube = iris.load_cube('/home/kobby/Desktop/pr_WFDEI_1979-2013_0.5x0.5_day_MPI-ESM-LR_west-africa_historical_r1i1p1_full.nc')
    #print mycube
    mycube_wafr = mycube.intersection(latitude=(2.0, 12.0), longitude=(-20.0, 20.0))
    #iris.coord_categorisation.add_day_of_month(mycube_wafr, 'time',name='day_of_month')
    iris.coord_categorisation.add_year(mycube_wafr, 'time',name='year')
    #iris.coord_categorisation.add_season(mycube_wafr, 'time',name='clim_season')
    iris.coord_categorisation.add_month_number(mycube_wafr, 'time',name='month_number')
    
    mycube_wafr.convert_units('kg m-2 day-1')
    ywetdays = calcWetDays(mycube_wafr, outpath) 
    print 'nc file saved'
    
if __name__ == '__main__': 
    main()
    
