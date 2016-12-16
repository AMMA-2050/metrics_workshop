import iris
import iris.coord_categorisation
        
def calcWetDays(incube, outfile):
    '''
    Inputs
        - incube : must have time dimension with year, month_number and season, and units in kg m-2 day-1
    Outputs
        - 
    '''
    
    outfile_month  = outfile.replace('.nc','month.nc')
    outfile_season = outfile.replace('.nc','season.nc')
   
    try:
        mwetdays=iris.load_cube(outfile_month)
        swetdays=iris.load_cube(outfile_season)
        
    except IOError:
        #pdb.set_trace()
        print incube
        iris.coord_categorisation.add_year(incube, 'time', name='year')
        iris.coord_categorisation.add_season_year(incube, 'time', name='season_year')
        iris.coord_categorisation.add_month_number(incube, 'time', name='month_number')
        incube.convert_units('kg m-2 day-1')
        
        print 'Calculating Number of Wet Days per Month'
        print incube
        wetdays = incube.aggregated_by(['year','month_number'], iris.analysis.COUNT, function = lambda values: values > 1.0 )
        print wetdays
        
        mwetdays = wetdays.aggregated_by('month_number', iris.analysis.MEAN)
        iris.save(mwetdays,outfile_month)
        
        swetdays = wetdays.aggregated_by('season_year', iris.analysis.MEAN)
        iris.save(swetdays,outfile_season)

    return([mwetdays,swetdays])