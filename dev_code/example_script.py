"""
This script compute seasonal mean of rainfall rate over West Africa
"""

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np

import iris
import iris.coord_categorisation
import iris.coords as coord
import iris.plot as iplt
import iris.quickplot as qplt

def main():
	## To ensure that netcdf loaded correctly 
    iris.FUTURE.netcdf_promote = True
    
    ## Paths and file name to be modified for your case
    PATH_MDL = '~/Bureau/Python352/'
    FILENAME = 'pr_WFDEI_1979-2013_0.5x0.5_day_IPSL-CM5A-LR_africa_rcp85_r1i1p1_full.nc'
    SEASONS = ('JFM','AMJ','JAS','OND')

	## Load data with iris package
    cube_global = iris.load_cube(PATH_MDL+FILENAME)

    ## Constraint over lat and lon for load data over specific array
    lat_WA = iris.Constraint(latitude=lambda cell: 0.0 <= cell <= 25.0)
    lon_WA = iris.Constraint(longitude=lambda cell: -20.0 <= cell <= 20.0)
    
    ## Extract data with multiple constraints and units conversion
    cube = cube_global.extract(lat_WA & lon_WA)   
    cube.convert_units('kg m-2 day-1')
    cube.rename('Precipitation_rate')
    cube.units='mm day-1'
    #print(cube)

    ## Add new time dimension before computing seasonal mean
    iris.coord_categorisation.add_season(cube, 'time', name='clim_season',seasons=SEASONS)
    iris.coord_categorisation.add_season_year(cube, 'time', name='season_year')
    annual_seasonal_mean = cube.aggregated_by(['clim_season', 'season_year'],iris.analysis.MEAN)

    idx=220

	## Set colobar, specific levels for contour
    levels = np.arange(20)
    c_map = cm.get_cmap('YlGnBu')

    fig,axes = plt.subplots(nrows=2, ncols=2)
    fig.suptitle('SEASONAL CYCLE (2006-2099)',  fontsize=12)
    
    ## Loop over season
    for iseas in SEASONS:
        #print(iseas)
        #type(iseas)
        seasons_constraint = iris.Constraint(clim_season=iseas)
        seasonal_data = annual_seasonal_mean.extract(seasons_constraint)
        seasonal_mean = seasonal_data.collapsed('time',iris.analysis.MEAN)
              
        idx+=1
        #print(idx)
        plt.subplot(idx)
        plt.title('IPSL-CM5A-LR   ' + iseas,  fontsize=10)
        iplt.contourf(seasonal_mean,levels,cmap = c_map)
        plt.gca().coastlines()
     
        plt.subplots_adjust(bottom=0.1, right=0.85, top=0.9)
        cax = plt.axes([0.9, 0.12, 0.04, 0.75])
        cbar = plt.colorbar(cax=cax)
        cbar.set_label(seasonal_mean.units)
        del seasonal_mean
    
if __name__ == '__main__':
    main()
