'''
calc_mean_temp
'''
import os
import iris
import iris.coord_categorisation 


def calc_mean_temp(cube, m_or_s, ncfile):
        
    if m_or_s == 'month':
        iris.coord_categorisation.add_month_number(cube, 'time', name='month')
        cubeout = cube.aggregated_by('month', iris.analysis.MEAN)
        cubeout.convert_units('Celsius') # convert unit

    if m_or_s == 'season':
        iris.coord_categorisation.add_season(cube, 'time', name='clim_season', seasons=('djf', 'mam', 'jja', 'son'))
        cubeout = cube.aggregated_by('clim_season', iris.analysis.MEAN)
        cubeout.convert_units('Celsius') # convert unit
    #qplt.pcolormesh(Temp[1])
    #plt.show
    #print cube.coord('month')
    #print cube.coord('month').shape
    #compute the monthly value
    #cubeout = cube.aggregated_by('month', iris.analysis.MEAN)
    #Tempss = cube.aggregated_by('clim_season', iris.analysis.MEAN)

    
    #iris.save(cubeout, ncfile)
        
    return(cubeout)