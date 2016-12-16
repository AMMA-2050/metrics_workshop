'''
This is a code to create a hovmoller and temeseries plots from CMIP5 data

Author: Youssouph Sane, Leeds at December 2016
'''
import numpy as np
import matplotlib.pyplot as plt
import iris
import iris.plot as iplt
import iris.quickplot as qplt
import iris.coord_categorisation
import iris.analysis.cartography
import matplotlib.dates as mdates
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm


def main():
     h11 = iris.load_cube(iris.sample_data_path('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/IPSL-CM5A-LR/historical/tasmax_WFDEI_1979-2013_0.5x0.5_day_IPSL-CM5A-LR_africa_historical_r1i1p1_full.nc'))
     ee85 = iris.load_cube(iris.sample_data_path('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/IPSL-CM5A-LR/rcp85/tasmax_WFDEI_1979-2013_0.5x0.5_day_IPSL-CM5A-LR_africa_rcp85_r1i1p1_full.nc'))
#     e45 = iris.load_cube(iris.sample_data_path('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/IPSL-CM5A-LR/rcp45/tasmax_WFDEI_1979-2013_0.5x0.5_day_IPSL-CM5A-LR_africa_rcp45_r1i1p1_full.nc'))
     h1 = h11.intersection(longitude=(-18.0, 0.0), latitude=(10.0, 20.0))
     e85 = ee85.intersection(longitude=(-18.0, 0.0), latitude=(10.0, 20.0))
     iris.coord_categorisation.add_year(h1, 'time', name='year')
     iris.coord_categorisation.add_year(e85, 'time', name='year')         
#     senegal = iris.Constraint(longitude=lambda v: -18 <= v <= -11,latitude=lambda v: 12 <= v <= 20)
#     pre_industrial = iris.load_cube(iris.sample_data_path('pre-industrial.pp'),senegal)
     h1.coord('latitude').guess_bounds()
     h1.coord('longitude').guess_bounds()
#     h1_grid_areas = iris.analysis.cartography.area_weights(h1)
     e85.coord('latitude').guess_bounds()
     e85.coord('longitude').guess_bounds()
 #    e85_grid_areas = iris.analysis.cartography.area_weights(e85)
#     print h1_grid_areas
#     e45.coord('latitude').guess_bounds()
#     e45.coord('longitude').guess_bounds()
#     e45_grid_areas = iris.analysis.cartography.area_weights(e45)
#     pre_industrial.coord('latitude').guess_bounds()
#     pre_industrial.coord('longitude').guess_bounds()
#     pre_grid_areas = iris.analysis.cartography.area_weights(pre_industrial)

#pre_industrial_mean = pre_industrial.collapsed(['latitude', 'longitude'],iris.analysis.MEAN,weights=pre_grid_areas)
#     pre_industrial_mean = pre_industrial.collapsed(['latitude', 'longitude'],iris.analysis.MEAN,weights=pre_grid_areas)
     h1_mean = h1.collapsed(['latitude', 'longitude'],iris.analysis.MEAN)
     e85_mean = e85.collapsed(['latitude', 'longitude'],iris.analysis.MEAN)
     h1_mean = h1_mean.aggregated_by('year',iris.analysis.MEAN)
     e85_mean = e85_mean.aggregated_by('year',iris.analysis.MEAN)
     print h1_mean.coord('year').points        
#     print h1_mean
#     e45_mean = e45.collapsed(['latitude', 'longitude'],iris.analysis.MEAN,weights=e45_grid_areas)
     time_past = h1_mean.coord('year').points
     time_future = e85_mean.coord('year').points
     plt.clf()
     ax1=plt.figure()
     h1mean = h1_mean.data
     e85mean = e85_mean.data
     h1meanyear = h1_mean.coord('year').points
     e85meanyear = e85_mean.coord('year').points

 #############################################################
 #
 # Make a custom color map to get one line with two colors
 #
 #############################################################
     cmap = ListedColormap(['k','r'])
     norm = BoundaryNorm([1950,2006,2100], cmap.N)
     segments = np.concatenate([h1mean,e85mean],axis = 0) 
     #print segments    
     years = np.concatenate([h1meanyear,e85meanyear],axis = 0)
     segments1 = np.array([segments,years]).T.reshape(-1,1,2)
     segments = np.concatenate([segments1[:-1], segments1[1:]], axis=1)
     print segments1
     lc = LineCollection(segments, cmap = cmap, norm = norm)
     lc.set_array(years)
     lc.set_linewidth(3)
     fig1 = plt.figure()
     plt.gca().add_collection(lc)
     plt.xlabel('Year')
     plt.ylabel('Temperature (K)')
     plt.title('Senegal mean air temperature', fontsize=18)
     plt.show()
     
#     print len(time_past), len(time_future), h1mean.shape, e85mean.shape
#     cubelist = iris.cube.CubeList([h1_mean,e85_mean])
#     longcube = cubelist.concatenate()[0]
#     print longcube.coord('year').points
#     label = ['1950', '1960', '1970', '1980', '1990', '2000', '2010', '2020', '2030', '2040', '2050', '2060', '2070', '2080', '2090', '2100']
#     plt.plot(time_past[:],h1mean[0:len(time_past)], label='Historical', lw=1.5, color='black')
#     plt.plot(time_future[:],e85mean[0:len(time_future)], label='rcp85 scenario', lw=1.5, color='red')
#     ax1.set_xlabel('Metric 1')  # label x and y axes
#     ax1.set_ylabel('Metric 2')
#     plt.gca().xaxis.set_major_locator(mdates.YearLocator(10))
#     ax1.set_legend(fontsize=10, loc='best')
#     qplt.plot(e45_mean, label='rcp45 scenario', lw=1.5, color='blue')

#plt.axhline(y=pre_industrial_mean.data, color='gray', linestyle='dashed',label='pre-industrial', lw=1.5)
#     plt.axhline(y=pre_industrial_mean.data, color='gray', linestyle='dashed',label='pre-industrial', lw=1.5)
#     observed = e85_mean[:np.argmin(np.isclose(e85_mean.data, h1_mean.data))]
#     qplt.plot(observed, label='observed', color='black', lw=1.5)
     #plt.legend(loc="upper left")

#     plt.xlabel('Time / year')

#     plt.grid()

#     plt.show()


if __name__ == '__main__':
    main()
