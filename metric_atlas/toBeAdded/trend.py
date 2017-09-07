#!/usr/local/sci/bin/python2.7

import os, sys
import matplotlib

###
#Use this for running on SPICE ...
hname = os.uname()[1]
if not hname.startswith('eld') and not hname.startswith('els'):
    matplotlib.use('Agg')
###
sys.path.append('/Users/ajh235/Work/github/metrics_workshop/metric-GUI/')
from make_big_cube import make_big_cube
import iris
import iris.coord_categorisation
import numpy as np
import numpy.ma as ma
import cf_units
from scipy import stats
import matplotlib.pyplot as plt
import iris.quickplot as qplt
from datetime import datetime, timedelta
from pylab import plot, title, show , legend
import glob
import pdb

iris.FUTURE.netcdf_no_unlimited = True
iris.FUTURE.netcdf_promote = True

def subsetByTime(cube, start_int, end_int):
    
    time_constraint = iris.Constraint(year=lambda cell: start_int < cell <= end_int)
    subset = cube.extract(time_constraint)
    
    return(subset)

def getDomain(name):
    boundary_dictionary = {'West_Africa': [-10., 10., 5., 25.],
                       'Senegal': [-20., -13., 12.5, 17.5],
                       'Burkina_Faso': [-14., -9., 8., 12.],
                       'Sahel': [-10., 10., 8., 12.],
                       'West_Sahel': [-15.9375, -4.6875, 11.875, 18.125],
                       'East_Sahel': [15., 34.6875, 11.875, 18.125],
                       'CenEast_Sahel': [-4.6875, 34.6875, 11.875, 18.125],
                       'Guinea_Coast': [-10., 10., 4., 6.]
                       }
    return(boundary_dictionary[name])

def domainNameLookup(name):
    domain_dict = {'West_Africa': "West Africa",
                       'Senegal': "Senegal",
                       'Burkina_Faso': "Burkina Faso",
                       'Sahel': "Sahel",
                       'West_Sahel': "West Sahel",
                       'East_Sahel': "East Sahel",
                       'CenEast_Sahel': "Central and Eastern Sahel",
                       'Guinea_Coast': "Guinea Coast"
                       }
    return(domain_dict[name])

    
def rand_jitter(arr):
    if max(arr) != min(arr):
        stdev = .05*(max(arr)-min(arr)) # The default, assuming that x has some values that vary.
    else:
        stdev = 0.1 # Varies +/- 0.3 around the median value
    return arr + np.random.randn(len(arr)) * stdev


def jitter(x, y, ax=None, s=20, c='r', marker='o', cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=0, verts=None, **kwargs):
    return ax.scatter(rand_jitter(x), rand_jitter(y), s=s, c=c, marker=marker, cmap=cmap, norm=norm, vmin=vmin, vmax=vmax, alpha=alpha, linewidths=linewidths, verts=verts, **kwargs) # hold=hold, 

def do_jitter(plotdata, axis):
    for i in np.arange(12):
        xvals = np.repeat(i+1, len(plotdata.data[:,i]))
        yvals = plotdata.data[:,i]
        jitter(x=xvals, y=yvals, ax=axis, alpha=0.2)
        
def plot_trends_boxplots(bc, v, reg):

    ylab = {'pr' : 'Precipitation Trend (mm/month/year)',
            'tas': 'Temperature Trend ($^\circ$C / year)'}

    suptitle = {'pr' : "Precipitation Trend (2010 to 2050) for "+domainNameLookup(reg),
                'tas': "Temperature Trend (2010 to 2050) for "+domainNameLookup(reg)}
    
    #search_string = '/Users/ajh235/Work/DataLocal/Projects/AMMA-2050/metrics/calc_trend_'+v+'_'+bc+'_rcp26'
    search_string = '/project/FCFA/CMIP5/bias_corrected/metrics/calc_trend_'+v+'_'+bc+'_rcp26'
    trends_rcp26 = make_big_cube(search_string)
    #search_string = '/Users/ajh235/Work/DataLocal/Projects/AMMA-2050/metrics/calc_trend_'+v+'_'+bc+'_rcp45'
    search_string = '/project/FCFA/CMIP5/bias_corrected/metrics/calc_trend_'+v+'_'+bc+'_rcp45'
    trends_rcp45 = make_big_cube(search_string)
    #search_string = '/Users/ajh235/Work/DataLocal/Projects/AMMA-2050/metrics/calc_trend_'+v+'_'+bc+'_rcp85'
    search_string = '/project/FCFA/CMIP5/bias_corrected/metrics/calc_trend_'+v+'_'+bc+'_rcp85'
    trends_rcp85 = make_big_cube(search_string)

    # Now, extract sub-region
    xmin, xmax, ymin, ymax = getDomain(reg)
    lonce = iris.coords.CoordExtent('longitude', xmin, xmax)
    latce = iris.coords.CoordExtent('latitude', ymin, ymax)
    
    slope_reg26 = trends_rcp26.intersection(lonce, latce)
    slope_reg45 = trends_rcp45.intersection(lonce, latce)
    slope_reg85 = trends_rcp85.intersection(lonce, latce)
    
    # Collapse cubes to give region average
    montrend26_mean = slope_reg26.collapsed(['latitude','longitude'], iris.analysis.MEAN)
    montrend45_mean = slope_reg45.collapsed(['latitude','longitude'], iris.analysis.MEAN)
    montrend85_mean = slope_reg85.collapsed(['latitude','longitude'], iris.analysis.MEAN)

    fig, [axis0, axis1, axis2] = plt.subplots(nrows=3, ncols=1, figsize=(10,10), sharey=True, sharex=True)
    
    labels = ['J','F','M','A','M','J','J','A','S','O','N','D']
    axis0.plot((1, 12), (0, 0), c='lightgrey')
    do_jitter(montrend26_mean.data, axis0)
    bp = axis0.boxplot(montrend26_mean.data, sym='', patch_artist=True) # , labels=labels
    #bp['boxes'].set(color = 'darkgrey', facecolor = 'darkgrey')
    #bp['medians'].set(alpha=0.0)
    nmods = str(len(montrend26_mean.coord('model_name').points))
    axis0.set_title('rcp2.6 (n='+nmods+')', fontsize=12)
    

    axis1.plot((1, 12), (0, 0), c='lightgrey')
    do_jitter(montrend45_mean.data, axis1)
    axis1.boxplot(montrend45_mean.data, sym='') # , labels=labels
    nmods = str(len(montrend45_mean.coord('model_name').points))
    axis1.set_title('rcp4.5 (n='+nmods+')', fontsize=12)
    axis1.set_ylabel(ylab[v], fontsize=12)

    axis2.plot((1, 12), (0, 0), c='lightgrey')
    do_jitter(montrend85_mean.data, axis2)
    axis2.boxplot(montrend85_mean.data, sym='') # , labels=labels
    nmods = str(len(montrend85_mean.coord('model_name').points))
    axis2.set_title('rcp8.5 (n='+nmods+')', fontsize=12)
    axis2.set_xticklabels(labels) # np.arange(1,13), 
    axis2.set_xlabel('Month', fontsize=12)

    #pdb.set_trace()
    
    #for i in np.arange(12):
        #xvals = np.repeat(i+1, len(montrend85_mean.data[:,i]))
        #yvals = montrend85_mean.data[:,i]
        #jitter(x=xvals, y=yvals, ax=axis2, alpha=0.2)
    
    fig.suptitle(suptitle[v], fontsize=14)
    fig.subplots_adjust(hspace=0.2)
    
    fig.savefig('/project/FCFA/CMIP5/bias_corrected/metrics/plots/annual_trend-'+bc+'-allscenarios-allmonths-'+v+'_'+reg+'_monthly_trend_boxplots.png')
    print 'Output: ' + '/project/FCFA/CMIP5/bias_corrected/metrics/plots/annual_trend-'+bc+'-allscenarios-allmonths-'+v+'_'+reg+'_monthly_trend_boxplots.png'
    # fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(10,12), sharey=True, sharex=True)
    # axes[0,0]

def calcTrend(bc, sc, v, reg, inpath, outpath, overwrite):

    calc_file = 'calc_trend'
    filepath = inpath+'/'+str(bc)+'/*/'+str(sc)+'/'+str(v)+'*.nc'
    infiles = glob.glob(filepath)

    for ifile in infiles:

        nme = ifile.split(os.sep)[-3]
        nc_file = outpath + str(calc_file) + '_' +v+ '_' + str(bc) + '_' + str(sc) + '_' + str(nme) + '.nc'

        #print nme

        if not os.path.exists(nc_file) or overwrite:
            
            print 'Calculating: ' + bc  + ', ' + v  + ', ' + reg  + ', ' + sc
            cube_orig = iris.load_cube(ifile)
            iris.coord_categorisation.add_month_number(cube_orig, 'time', name='month_number')
            iris.coord_categorisation.add_year(cube_orig, 'time', name='year')
            incube = subsetByTime(cube_orig, 2010, 2050)

            # NB: Units are kg/m2/s
            if incube.units == 'unknown':
                incube.units = cf_units.Unit('kg m-2 s-1')

            if v == 'pr':
                incube_ym = incube.aggregated_by(['year','month_number'], iris.analysis.SUM)
                incube_ym.convert_units('kg m-2 month-1')

            if v == 'tas':
                incube_ym = incube.aggregated_by(['year','month_number'], iris.analysis.MEAN)
                #incube_ym.convert_units('kg m-2 month-1')
                
            # Check that aggregating first, then regressing is the same as this approach

            slopedata1mon = np.zeros(incube_ym[0].shape).reshape((1,incube_ym[0].shape[0], incube_ym[0].shape[1]))
            slopedata = np.repeat(slopedata1mon, 12, axis=0)
            moncoord = iris.coords.DimCoord(points=np.arange(1,13), long_name='month_number', units='1')
            slope = iris.cube.Cube(slopedata, long_name='Trend', units=incube_ym.units, dim_coords_and_dims=[(moncoord, 0), (incube.coord('latitude'), 1), (incube.coord('longitude'), 2)])
            for mon in np.arange(1,13):
                #print mon
                slicer = iris.Constraint(month_number=lambda cell: cell == mon)
                incube1mon = incube_ym.extract(slicer)
                for x in np.arange(len(incube.coord('longitude').points)):
                    for y in np.arange(len(incube.coord('latitude').points)):
                        if np.all(incube1mon.data[:,y,x].mask):
                            slope.data[mon-1,y,x] = ma.masked
                        else:
                            reg = stats.linregress(np.arange(incube1mon.shape[0]), incube1mon.data[:,y,x])
                            #pdb.set_trace()
                            slope.data[mon-1,y,x] = reg[0] # NB: slope, intercept, r-value, pvalue, std_err # for py34: reg.slope

            #print 'Saving: ' + nc_file
            iris.save(slope, nc_file)
    
def main():
    
    #inpath = '/Users/ajh235/Work/DataLocal/Projects/AMMA-2050'
    #outpath = '/Users/ajh235/Work/DataLocal/Projects/AMMA-2050/metrics/'
    inpath = '/project/FCFA/CMIP5/bias_corrected/WA_data'
    outpath = '/project/FCFA/CMIP5/bias_corrected/metrics/'
    biascorr = ['BC_0.5x0.5']
    scenarios = ['rcp26', 'rcp45', 'rcp85']
    variables = ['pr', 'tas'] # ['tas']
    regions = ['Senegal', 'Burkina_Faso', 'West_Sahel','CenEast_Sahel','East_Sahel']
    overwrite = False

    # NB: incube must be a daily time series
    # in_file_wfdei = "/Users/ajh235/Work/DataLocal/Projects/AMMA-2050/WFDEI/pr_daily_WFDEI_full.nc_west-africa.nc"

    for bc in biascorr:
        for v in variables:
            for reg in regions:
                for sc in scenarios:
                    
                    calcTrend(bc, sc, v, reg, inpath, outpath, overwrite)

                print 'Plotting: ' + bc + ', ' + v + ', ' + reg
                plot_trends_boxplots(bc, v, reg)
                    

            
if __name__ == "__main__":
    main()
    
