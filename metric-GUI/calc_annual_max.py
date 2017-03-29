##############################################################

#SCRIPT TO CALCULATE ANNUAL MAXIMUM

##############################################################
import itertools
import iris
import iris.coord_categorisation
    
def annMax(incube, outpath):
    '''
    Inputs
        - incube : must have time dimension with year, month_number and season, and units in kg m-2 day-1
    Outputs
        - ?
    '''
    
    try:
        
        ymaximum=iris.load_cube(outpath+'mean_annmax.nc')
    except IOError:
    
        print 'Calculating Annual Maximum'
        print incube
               
        annmax = incube.aggregated_by(['year'], iris.analysis.MAX)
        print annmax
                        
        ymaximum = annmax.aggregated_by('year', iris.analysis.MEAN)
        iris.save(ymaximum,outpath+'mean_annmax.nc')
    return(ymaximum)

def main():
    
    outpath = '/home/kobby/Desktop/'
    # this is the function that controls everything 
    mycube = iris.load_cube('/home/kobby/Desktop/pr_WFDEI_1979-2013_0.5x0.5_day_MPI-ESM-LR_west-africa_historical_r1i1p1_full.nc')
    #print mycube
    mycube_wafr = mycube.intersection(latitude=(2.0, 12.0), longitude=(-20.0, 20.0))
    #iris.coord_categorisation.add_day_of_month(mycube_wafr, 'time',name='day_of_month')
    iris.coord_categorisation.add_year(mycube_wafr, 'time',name='year')
    #iris.coord_categorisation.add_season(mycube_wafr, 'time',name='clim_season')
    #iris.coord_categorisation.add_month_number(mycube_wafr, 'time',name='month_number')
    
    mycube_wafr.convert_units('kg m-2 day-1')
    ymaximum = annMax(mycube_wafr, outpath) 
    print 'nc file saved'
    
if __name__ == '__main__': 
    main()
    
