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
        mwetdays=iris.load_cube(outpath+'meanwetdays_permonth.nc')
        swetdays=iris.load_cube(outpath+'meanwetdays_perseason.nc')
    except IOError:
    
        print 'Calculating Number of Wet Days per Month'
        print incube
        wetdays = incube.aggregated_by(['year','month_number'], iris.analysis.COUNT, function = lambda values: values > 1.0 )
        print wetdays
        
        mwetdays = wetdays.aggregated_by('month_number', iris.analysis.MEAN)
        iris.save(mwetdays,outpath+'meanwetdays_permonth.nc')
        
        swetdays = wetdays.aggregated_by('season_year', iris.analysis.MEAN)
        iris.save(swetdays,outpath+'meanwetdays_perseason.nc')
    return(swetdays)

def main():
    
    outpath = '/nfs/a266/earv060/wetdays/'
    # this is the function that controls everything 
    mycube = iris.load_cube('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/MIROC5/historical/pr_WFDEI_1979-2013_0.5x0.5_day_MIROC5_africa_historical_r1i1p1_full.nc')
    #print mycube
    mycube_wafr = mycube.intersection(latitude=(2.0, 12.0), longitude=(-20.0, 20.0))
    iris.coord_categorisation.add_year(mycube_wafr, 'time',name='year')
    iris.coord_categorisation.add_season_year(mycube_wafr, 'time',name='season_year')
    iris.coord_categorisation.add_month_number(mycube_wafr, 'time',name='month_number')
    mycube_wafr.convert_units('kg m-2 day-1')
    mwetdays = calcWetDays(mycube_wafr, outpath) 
    print 'nc file saved'
    
if __name__ == '__main__': 
    main()
       
        
        
        
        