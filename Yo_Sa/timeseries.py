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


def main():
     iris.FUTURE.netcdf_promote=True
     h11 = iris.load_cube(iris.sample_data_path('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/IPSL-CM5A-LR/historical/tasmax_WFDEI_1979-2013_0.5x0.5_day_IPSL-CM5A-LR_africa_historical_r1i1p1_full.nc'))
     ee85 = iris.load_cube(iris.sample_data_path('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/IPSL-CM5A-LR/rcp85/tasmax_WFDEI_1979-2013_0.5x0.5_day_IPSL-CM5A-LR_africa_rcp85_r1i1p1_full.nc'))
    # ee45 = iris.load_cube(iris.sample_data_path('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/IPSL-CM5A-LR/rcp45/tasmax_WFDEI_1979-2013_0.5x0.5_day_IPSL-CM5A-LR_africa_rcp45_r1i1p1_full.nc'))
     #ee45 = iris.load_cube(iris.sample_data_path('/nfs/a266/data/CMIP5_AFRICA/BC_0.5x0.5/IPSL-CM5A-LR/rcp26/tasmax_WFDEI_1979-2013_0.5x0.5_day_IPSL-CM5A-LR_africa_rcp26_r1i1p1_full.nc'))
#     h11.convert_units('Celsius') # convert unit
#     ee85.convert_units('Celsius') # convert unit
#     ee45.convert_units('Celsius') # convert unit
     h1 = h11.intersection(longitude=(-18.0, 0.0), latitude=(10.0, 20.0))
     e85 = ee85.intersection(longitude=(-18.0, 0.0), latitude=(10.0, 20.0))
    # e45 = ee45.intersection(longitude=(-18.0, 0.0), latitude=(10.0, 20.0))
     iris.coord_categorisation.add_year(h1, 'time', name='year')
     iris.coord_categorisation.add_year(e85, 'time', name='year') 
     h1.coord('latitude').guess_bounds()
     h1.coord('longitude').guess_bounds()
     e85.coord('latitude').guess_bounds()
     e85.coord('longitude').guess_bounds()
    # e45.coord('latitude').guess_bounds()
    # e45.coord('longitude').guess_bounds()
     h1_mean = h1.collapsed(['latitude', 'longitude'],iris.analysis.MEAN)
     e85_mean = e85.collapsed(['latitude', 'longitude'],iris.analysis.MEAN)
    # e45_mean = e45.collapsed(['latitude', 'longitude'],iris.analysis.MEAN)
     h1_mean = h1_mean.aggregated_by('year',iris.analysis.MEAN)
   #  e45_mean = e45_mean.aggregated_by('year',iris.analysis.MEAN)
     e85_mean = e85_mean.aggregated_by('year',iris.analysis.MEAN)
     print h1_mean.coord('year').points 
     print e85_mean.coord('year').points
    # print e45_mean.coord('year').points
#     axe1 = h1_mean.coord('year').points
#     axe2 = e85_mean.coord('year').points    
#     e45_mean = e45.collapsed(['latitude', 'longitude'],iris.analysis.MEAN,weights=e45_grid_areas)
     time_past = h1_mean.coord('year').points
     time_future = e85_mean.coord('year').points
#     time_future1 = e45_mean.coord('year').points
     plt.clf()
     plt.figure()
     h1mean = h1_mean.data
     e85mean = e85_mean.data
   #  e45mean = e45_mean.data
     print len(e85mean)
   #  print len(e45mean)
     plt.gca().xaxis.set_major_locator(mdates.YearLocator(10))
     print len(time_past), len(time_future), h1mean.shape, e85mean.shape
     cubelist = iris.cube.CubeList([h1_mean,e85_mean])
     longcube = cubelist.concatenate()[0]
     print longcube.coord('year')
     x = np.arange(1950,2100,10)
     labels = ['1950', '1960', '1970', '1980', '1990', '2000', '2010', '2020', '2030', '2040', '2050', '2060', '2070', '2080', '2090', '2100']
     #plt.plot(time_past[:],h1mean[0:len(time_past)], label='Historical', lw=1.5, color='black')
     plt.plot(np.arange(1950,2006,1),h1mean[0:len(time_past)], label='Historical', lw=1.5, color='black')
     #plt.plot(time_future[:],e85mean[0:len(time_future)], label='rcp85 scenario', lw=1.5, color='red')
     plt.plot(np.arange(2006,2100,1),e85mean[0:len(time_future)], label='rcp85 scenario', lw=1.5, color='red')
   #  plt.plot(np.arange(2006,2100,1),e45mean[0:len(time_future1)], label='rcp45 scenario', lw=1.5, color='blue')
     plt.xticks(x, labels, rotation='vertical')
     plt.xlim([1950,2100])
     plt.xlabel('Annees')  # label x and y axes
     plt.ylabel('Temperature')
     plt.legend(fontsize=10, loc='best')
#     qplt.plot(e45_mean, label='rcp45 scenario', lw=1.5, color='blue')

#plt.axhline(y=pre_industrial_mean.data, color='gray', linestyle='dashed',label='pre-industrial', lw=1.5)
#     plt.axhline(y=pre_industrial_mean.data, color='gray', linestyle='dashed',label='pre-industrial', lw=1.5)
#     observed = e85_mean[:np.argmin(np.isclose(e85_mean.data, h1_mean.data))]
#     qplt.plot(observed, label='observed', color='black', lw=1.5)
     #plt.legend(loc="upper left")
     plt.title('Senegal mean air temperature', fontsize=18)

     plt.xlabel('Time / year')

     plt.grid()

     iplt.show()


if __name__ == '__main__':
    main()
