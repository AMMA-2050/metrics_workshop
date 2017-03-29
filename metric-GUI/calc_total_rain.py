####################################################################

#SCRIPT TO CALCULATE RAINFALL TOTAL ACROSS ALL WET DAYS IN A SEASON
#AND THE AVERAGE RAINFALL PER WET DAY IN A SEASON

####################################################################

import itertools
import iris
import iris.coord_categorisation
    
def totRain(incube, outpath):
    '''
    Inputs
        - incube : must have time dimension with year, month_number and season, and units in kg m-2 day-1
    Outputs
        - ?
    '''
    
    try:
        
        seatotal=iris.load_cube(outpath+'meantotrain_perseason.nc')
        swetdays=iris.load_cube(outpath+'meanwetdays_perseason.nc')
        SavRainfall=iris.load_cube(outpath+'meanrainfall_perwetday.nc')
    except IOError:
    
        print 'Calculating Total Rainfall per Season'
        print incube
               
        totrain = incube.aggregated_by(['clim_season','season_year'], iris.analysis.SUM)
        print totrain
                        
        seatotal = totrain.aggregated_by(['clim_season','season_year'], iris.analysis.MEAN)
        iris.save(seatotal,outpath+'meantotrain_perseason.nc')
        
        wetdays = incube.aggregated_by(['clim_season','season_year'], iris.analysis.COUNT, function = lambda values: values > 1.0 )
        print wetdays
        
        swetdays = wetdays.aggregated_by(['clim_season','season_year'], iris.analysis.MEAN)
        iris.save(swetdays,outpath+'meanwetdays_perseason.nc')
        
        SavRainfall = seatotal / swetdays
        iris.save(SavRainfall,outpath+'meanrainfall_perwetday.nc')
    return(SavRainfall)

def main():
    
    outpath = '/home/kobby/Desktop/'
    # this is the function that controls everything 
    mycube = iris.load_cube('/home/kobby/Desktop/pr_WFDEI_1979-2013_0.5x0.5_day_MPI-ESM-LR_west-africa_historical_r1i1p1_full.nc')
    #print mycube
    mycube_wafr = mycube.intersection(latitude=(2.0, 12.0), longitude=(-20.0, 20.0))
    iris.coord_categorisation.add_season_year(mycube_wafr, 'time',name='season_year')
    #iris.coord_categorisation.add_year(mycube_wafr, 'time',name='year')
    iris.coord_categorisation.add_season(mycube_wafr, 'time',name='clim_season')
    #iris.coord_categorisation.add_month_number(mycube_wafr, 'time',name='month_number')
    
    mycube_wafr.convert_units('kg m-2 day-1')
    SavRainfall = totRain(mycube_wafr, outpath) 
    print 'nc file saved'
    
if __name__ == '__main__': 
    main()
    
