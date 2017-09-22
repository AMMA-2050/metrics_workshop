"""
This module contains all plotting functions for the climate metrics atlas.
Plots called *_single show single scenarios while plots called *_scenarios show all scenarios at once.
Anomalies:
All plots have an "anomaly" option to calculate the difference between historical and future period.
Anomaly percentage change is with respect to the historical period.
Time periods are as defined in constants.py for the FUTURE and HIST variables.
(e.g. time period 1950-2000 (historical) and 2040-2069 (scenario))

C. Klein (CEH) & Andy Hartley (Met Office) 2017
"""
import os
import matplotlib as mpl
if not 'eld' in os.uname()[1]:
    mpl.use('Agg')
import iris
import matplotlib.pyplot as plt
import numpy as np
import os
import constants as cnst
import labeller as lblr
import sys
import glob
import utils
import cartopy
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import pdb

print mpl.__version__

def rand_jitter(arr):
    if max(arr) != min(arr):
        stdev = .05*(max(arr)-min(arr)) # The default, assuming that x has some values that vary.
    else:
        stdev = 0.1 # Varies +/- 0.3 around the median value
    return arr + np.random.randn(len(arr)) * stdev

def jitter(x, y, ax=None, s=20, c='r', marker='o', cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=0, verts=None, **kwargs):
    return ax.scatter(rand_jitter(x), rand_jitter(y), s=s, c=c, marker=marker, cmap=cmap, norm=norm, vmin=vmin, vmax=vmax, alpha=alpha, linewidths=linewidths, verts=verts, **kwargs) # hold=hold, 


def do_jitter(plotdata, axis):
    # Assumes that plotdata is a list of lists. Each element of the first dimension refers to a scenario (on the x-axis of a boxplot)
    for i in np.arange(len(plotdata)):
        xvals = np.repeat(i+1, len(plotdata[i]))
        yvals = plotdata[i]
        jitter(x=xvals, y=yvals, ax=axis, alpha=0.2)


def map_percentile_single(incubes, outpath, region, anomaly=False):
    """
    Produces maps for individual scenarios of the 10th and 90th percentile of the model ensemble.
    :param incubes: single 2d file of a multi-model metric cube
    :param outpath: the path where the plot is saved
    :param region: the region dictionary as defined in constants
    :param anomaly: boolean, switch for anomaly calculation
    :return: plot
    """
    ano = glob.glob(incubes + '_2d.nc')
    if len(ano) != 1:
        sys.exit('Found too many files, need one file')
    ano = ano[0]

    fdict = utils.split_filename_path(ano)
    scen = fdict['scenario']
    metric = fdict['metric']
    variable = fdict['variable']
    season = fdict['season']
    bc = fdict['bc_res']

    if (anomaly == True) & (scen == 'historical'):
        return

    vname = cnst.VARNAMES[fdict['variable']]
    cube = iris.load_cube(ano)

    if anomaly:

        ano_hist = ano.replace(fdict['scenario'], 'historical')
        hist = iris.load_cube(ano_hist)

        data = utils.anomalies(hist, cube, percentage=False)
        data_perc = utils.anomalies(hist, cube, percentage=True)

        data_perc = data_perc.collapsed('model_name', iris.analysis.PERCENTILE, percent=[10, 90])
        data = data.collapsed('model_name', iris.analysis.PERCENTILE, percent=[10, 90])

        plot_dic1 = {'data': data,
                     'ftag': scen + 'Anomaly',
                     'cblabel': 'anomaly',
                     'levels': (utils.datalevels_ano(data[0].data), utils.datalevels_ano(data[1].data)),
                     'cmap': 'RdBu'
                     }

        plot_dic2 = {'data': data_perc,
                     'ftag': scen + 'PercentageAnomaly',
                     'cblabel': 'percentageAnomaly',
                     'levels': (utils.datalevels_ano(data_perc[0].data), utils.datalevels_ano(data_perc[1].data)),
                     'cmap': 'RdBu'
                     }

        toplot = [plot_dic1, plot_dic2]

    else:

        data = cube
        data = data.collapsed('model_name', iris.analysis.PERCENTILE, percent=[10, 90])

        plot_dic1 = {'data': data,
                     'ftag': scen,
                     'cblabel': '',
                     'levels': (utils.datalevels(data[0].data), utils.datalevels(data[1].data)),
                     'cmap': 'viridis'
                     }

        toplot = [plot_dic1]

    for p in toplot:
        f = plt.figure(figsize=lblr.getFigSize(region[0], 'map'), dpi=300)
        siz = 6
        lon = data.coord('longitude').points
        lat = data.coord('latitude').points

        ax1 = f.add_subplot(211, projection=ccrs.PlateCarree())

        #ax1.set_title(vname + ': ' + fdict['metric'], fontsize=10)
        ax1.set_title('90th Percentile')

        map1 = ax1.contourf(lon, lat, p['data'][1].data, transform=ccrs.PlateCarree(), cmap=p['cmap'],
                            levels=p['levels'][1], extend='both')
        ax1.coastlines()
        # Gridlines
        siz = 6
        xl = ax1.gridlines(draw_labels=True);
        xl.xlabels_top = False
        xl.ylabels_right = False
        xl.xformatter = LONGITUDE_FORMATTER
        xl.yformatter = LATITUDE_FORMATTER
        xl.xlabel_style = {'size': siz, 'color': 'k'}
        xl.ylabel_style = {'size': siz, 'color': 'k'}
        # Countries
        ax1.add_feature(cartopy.feature.BORDERS, linestyle='--');
        cb = plt.colorbar(map1, format='%1.1f')
        #cb.set_label('10th percentile ' + p['cblabel'])
        cb.set_label(lblr.getYlab(metric, variable, anom=p['cblabel']))

        ax2 = f.add_subplot(212, projection=ccrs.PlateCarree())
        try:
            map2 = ax2.contourf(lon, lat, p['data'][0].data, transform=ccrs.PlateCarree(), cmap=p['cmap'],levels=p['levels'][0], extend='both')
        except:
            # TODO : Fix bug here for annualMeanRainyDay / JAS / rcp85 / anomaly
            # Seems that there's an error in picking up the contour levels. They come out as [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
#            pdb.set_trace()
            continue
        ax2.coastlines()
        ax2.set_title('10th Percentile')
        # Gridlines
        xl = ax2.gridlines(draw_labels=True, );
        xl.xlabels_top = False
        xl.ylabels_right = False
        xl.xformatter = LONGITUDE_FORMATTER
        xl.yformatter = LATITUDE_FORMATTER
        xl.xlabel_style = {'size': siz, 'color': 'k'}
        xl.ylabel_style = {'size': siz, 'color': 'k'}
        # Countries
        ax2.add_feature(cartopy.feature.BORDERS, linestyle='--');
        cb = plt.colorbar(map2, format='%1.1f')
        cb.set_label(lblr.getYlab(metric, variable, anom=p['cblabel']))

        #plt.tight_layout()
        #f.suptitle('Long figure title')
        f.suptitle(lblr.getTitle(metric, variable, season, scen, bc, region[1], anom=p['cblabel']))
        f.subplots_adjust(left=0.05)
        plt.savefig(outpath + os.sep + fdict['metric'] + '_' + fdict['variable'] + '_' +
                    fdict['bc_res'] + '_' + fdict['season'] + '_' + region[0] + '_mapPerc_' + p['ftag'] + '.png')

        plt.close(f)


def boxplot_scenarios(incubes, outpath, region, anomaly=False):
    """
       Produces a boxplot with a box for each scenario, indicating the model spread.
       :param incubes: wildcard path to all tseries multi-model cubes
       :param outpath: the path where the plot is saved
       :param region: the region dictionary as defined in constants
       :param anomaly: boolean, switch for anomaly calculation
       :return: plot
       """
    ano_list = glob.glob(incubes + '_tseries.nc')
    ano_list = utils.order(ano_list)

    ldata = []
    scen = []
    perc = []
    for ano in ano_list:

        fdict = utils.split_filename_path(ano)
        metric = fdict['metric']
        variable = fdict['variable']
        season = fdict['season']
        scenario = fdict['scenario']
        bc = fdict['bc_res']
        
        if (anomaly == True) & (fdict['scenario'] == 'historical'):
            continue

        vname = cnst.VARNAMES[fdict['variable']]
        cube = iris.load_cube(ano)
        cube = utils.time_slicer(cube, fdict['scenario'])
        cube = cube.collapsed('year', iris.analysis.MEAN)

        if anomaly:
            ano_hist = ano.replace(fdict['scenario'], 'historical')
            hist = iris.load_cube(ano_hist)
            hist = utils.time_slicer(hist, 'historical')

            hist = hist.collapsed('year', iris.analysis.MEAN)

            data = utils.anomalies(hist, cube, percentage=False)
            data_perc = utils.anomalies(hist, cube, percentage=True)

            an = 'anomaly'
            ylabel = lblr.getYlab(metric, variable, anom='absolute')
            #ylabel = vname + ' anomaly: ' + fdict['metric']

            an_p = 'percentageAnomaly'
            #ylabel_p = vname + ' anomaly percentage: ' + fdict['metric']
            ylabel_p = lblr.getYlab(metric, variable, anom='percentage')
            dat_perc = np.ndarray.tolist(data_perc.data)
            perc.append(dat_perc)

        else:
            data = cube
            an = 'scenarios'
            #ylabel = vname + ': ' + fdict['metric']
            ylabel = lblr.getYlab(metric, variable, anom=None)

        dat = data.data
        dat = np.ndarray.tolist(dat)
        ldata.append(dat)

        scen.append(fdict['scenario'])

    plot_dic1 = {'data': ldata,
                 'xlabel': scen,
                 'ftag': an,
                 'ylabel': ylabel}

    toplot = [plot_dic1]

    if anomaly:
        plot_dic2 = {'data': perc,
                     'xlabel': scen,
                     'ftag': an_p,
                     'ylabel': ylabel_p}

        toplot = [plot_dic1, plot_dic2]

    for p in toplot:

        f = plt.figure(figsize=(9,7))

        #do_jitter(p['data'], f.gca())
        try:
            bp = plt.boxplot(p['data'], labels=p['xlabel'], sym='', patch_artist=True, notch=False)
        except:
            pdb.set_trace()
        plt.title(lblr.getTitle(metric, variable, season, scenario, bc, region[1], anom=p['ftag'])) # (region[1])
        plt.xlabel('Scenario')
        plt.ylabel(p['ylabel'])

        for median, box in zip(bp['medians'], bp['boxes']):
            box.set(facecolor='none')
            median.set(linewidth=0) #median.set(color='k', linewidth=2)

        for id, d in enumerate(p['data']):
            plt.scatter([id + 1] * len(d), d, marker='_', color='darkgreen')

        plt.savefig(outpath + os.sep + fdict['metric'] + '_' + fdict['variable'] + '_' +
                    fdict['bc_res'] + '_' + fdict['season'] + '_' + region[0] + '_allModelBoxplot_' + p[
                        'ftag'] + '.png')

        plt.close(f)



def barplot_scenarios(incubes, outpath, region, anomaly=False):
    """
       Barplot showing the average of the (anomaly) metric over the climatological period for all
       individual models and scenarios.
       :param incubes: wildcard path to all tseries multi-model cubes
       :param outpath: the path where the plot is saved
       :param region: the region dictionary as defined in constants
       :param anomaly: boolean, switch for anomaly calculation
       :return: plot
       """
    # This creates a list of '*allModels_tseries.nc' files, one element for each scenario
    ano_list = glob.glob(incubes + '_tseries.nc')
    ano_list = utils.order(ano_list) 
    
    ldata = []
    scen = []
    perc = []
    lmodels = []
    for ano in ano_list:

        fdict = utils.split_filename_path(ano)
        scenario = fdict['scenario']
        metric = fdict['metric']
        variable = fdict['variable']
        season = fdict['season']
        bc = fdict['bc_res']

        if (anomaly == True) & (fdict['scenario'] == 'historical'):
            continue

        #vname = cnst.VARNAMES[fdict['variable']]
        cube = iris.load_cube(ano)
        cube = utils.time_slicer(cube, fdict['scenario'])
        cube = cube.collapsed('year', iris.analysis.MEAN)
        lmodels.append(np.ndarray.tolist(cube.coord('model_name').points))

        if anomaly:
            ano_hist = ano.replace(fdict['scenario'], 'historical')
            hist = iris.load_cube(ano_hist)
            hist = utils.time_slicer(hist, 'historical')
            hist = hist.collapsed('year', iris.analysis.MEAN)

            data = utils.anomalies(hist, cube, percentage=False)
            data_perc = utils.anomalies(hist, cube, percentage=True)

            an = 'anomaly'
#            ylabel = ' anomaly'
            ylabel = lblr.getYlab(metric, variable, anom="anomaly")

            an_p = 'percentageAnomaly'
#            ylabel_p = 'percentage anomaly'
            ylabel_p = lblr.getYlab(metric, variable, anom="percentageAnomaly")
            dat_perc = np.ndarray.tolist(data_perc.data)
            perc.append(dat_perc)

        else:
            data = cube
            an = 'scenarios'
#            ylabel = vname
            ylabel = lblr.getYlab(metric, variable, anom="")

        dat = data.data
        dat = np.ndarray.tolist(dat)
        ldata.append(dat)

        scen.append(scenario)

    plot_dic1 = {'data': ldata,
                 'xlabel': scen,
                 'ftag': an,
                 'ylabel': ylabel,
                 'models': lmodels}

    toplot = [plot_dic1]

    if anomaly:
        plot_dic2 = {'data': perc,
                     'xlabel': scen,
                     'ftag': an_p,
                     'ylabel': ylabel_p,
                     'models': lmodels}

        toplot = [plot_dic1, plot_dic2]

    for p in toplot:

        if len(p['data']) < 4:
            xp = len(p['data'])
            yp = 1
            xx = 9
            yy = 9
        else:
            xp = 2
            yp = 2
            xx = 13
            yy = 8

        f = plt.figure(figsize=(xx, yy))

        for id in range(len(p['data'])):
            ax = f.add_subplot(xp, yp, id + 1)

            b = plt.bar(range(len(p['models'][id])), p['data'][id], align='edge', label=p['models'][id],
                        color='darkseagreen')

            # plt.subplots_adjust(bottom=0.8)
            xticks_pos = [0.65 * patch.get_width() + patch.get_xy()[0] for patch in b]

            plt.xticks(xticks_pos, p['models'][id], ha='right', rotation=45)

            plt.ylabel(p['ylabel'])
            plt.title(p['xlabel'][id])
            #plt.title(lblr.getTitle(metric, variable, season, scenario, bc, region[1], anom=p['ftag']))
            #plt.title(p['xlabel'][id] + ': ' + fdict['metric'] + ' ' + vname)

        plt.tight_layout(h_pad=0.2, rect=(0,0,1,0.92))
        plt.suptitle(lblr.getTitle(metric, variable, season, scen, bc, region[1], anom=p['ftag']))

        plt.savefig(outpath + os.sep + fdict['metric'] + '_' + fdict['variable'] + '_' +
                    fdict['bc_res'] + '_' + fdict['season'] + '_' + region[0] + '_allModelHisto_' + p[
                        'ftag'] + '.png')

        plt.close(f)


def nbModels_histogram_single(incubes, outpath, region, anomaly=False):
    """
    Histogram plot showing the number of models within different ranges of the metric (anomaly) value for a single scenario
   :param incubes: wildcard path to all tseries multi-model cubes
   :param outpath: the path where the plot is saved
   :param region: the region dictionary as defined in constants
   :param anomaly: boolean, switch for anomaly calculation
   :return: plot
   """
    ano = glob.glob(incubes + '_tseries.nc')
    if len(ano) != 1:
        sys.exit('Found too many files, need one file')
    ano = ano[0]

    fdict = utils.split_filename_path(ano)
    scen = fdict['scenario']
    metric = fdict['metric']
    variable = fdict['variable']
    season = fdict['season']
    bc = fdict['bc_res']

    if (anomaly == True) & (scen == 'historical'):
        return

    vname = cnst.VARNAMES[fdict['variable']]
    cube = iris.load_cube(ano)
    cube = utils.time_slicer(cube, fdict['scenario'])
    cube = cube.collapsed('year', iris.analysis.MEAN)

    if anomaly:
        ano_hist = ano.replace(fdict['scenario'], 'historical')
        hist = iris.load_cube(ano_hist)
        hist = utils.time_slicer(hist, 'historical')
        hist = hist.collapsed('year', iris.analysis.MEAN)

        data = utils.anomalies(hist, cube, percentage=False)
        data_perc = utils.anomalies(hist, cube, percentage=True)

        data = data.data
        data_perc = data_perc.data

        histo, h = np.histogram(data, bins=np.linspace(data.min(), data.max(), 10))
        histop, hp = np.histogram(data_perc, bins=np.linspace(data_perc.min(), data_perc.max(), 10))

        plot_dic1 = {'data': histo,
                     'ftag': scen + 'Anomaly',
                     'ylabel': lblr.getYlab(metric, variable, anom="anomaly"),
                     'bins': h
                     }

        plot_dic2 = {'data': histop,
                     'ftag': scen + 'PercentageAnomaly',
                     'ylabel': lblr.getYlab(metric, variable, anom="percentageAnomaly"),
                     'bins': hp
                     }

        toplot = [plot_dic1, plot_dic2]

    else:
        cube = cube.data
        histo, h = np.histogram(cube, bins=np.linspace(cube.min(), cube.max(), 10))
        plot_dic1 = {'data': histo,
                     'ftag': scen,
                     'ylabel': lblr.getYlab(metric, variable, anom=""),
                     'bins': h
                     }
        toplot = [plot_dic1]

    for p in toplot:
        f = plt.figure(figsize=lblr.getFigSize(None, 'nbModelHistogram'))
        ax = f.add_subplot(111)
        bin = p['bins']
        ax.bar(bin[0:-1] + ((bin[1::] - bin[0:-1]) / 2), p['data'], edgecolor='black', width=(bin[1::] - bin[0:-1]),
               align='edge', color='darkseagreen')

        ax.set_xlabel(p['ylabel'])
        ax.set_ylabel('Number of models')
        ax.set_title(lblr.getTitle(metric, variable, season, scen, bc, region[1], anom=p['ftag']))
        #ax.set_title(region[1] + ': ' + scen)
        plt.savefig(outpath + os.sep + fdict['metric'] + '_' + fdict['variable'] + '_' +
                    fdict['bc_res'] + '_' + fdict['season'] + '_' + region[0] + '_nbModelHistogram_' + p[
                        'ftag'] + '.png')
        plt.close(f)


def nbModels_histogram_scenarios(incubes, outpath, region, anomaly=False):
    """
       Histogram plot showing the number of models within different ranges of the metric (anomaly) value for ALL scenarios
      :param incubes: wildcard path to all tseries multi-model cubes
      :param outpath: the path where the plot is saved
      :param region: the region dictionary as defined in constants
      :param anomaly: boolean, switch for anomaly calculation
      :return: plot
      """
    ano_list = glob.glob(incubes + '_tseries.nc')
    ano_list = utils.order(ano_list)

    ldata = []
    scen = []
    perc = []

    for ano in ano_list:

        fdict = utils.split_filename_path(ano)
        scenario = fdict['scenario']
        metric = fdict['metric']
        variable = fdict['variable']
        season = fdict['season']
        bc = fdict['bc_res']

        if (anomaly == True) & (fdict['scenario'] == 'historical'):
            continue

        vname = cnst.VARNAMES[fdict['variable']]
        cube = iris.load_cube(ano)
        cube = utils.time_slicer(cube, fdict['scenario'])

        cube = cube.collapsed('year', iris.analysis.MEAN)

        if anomaly:
            ano_hist = ano.replace(fdict['scenario'], 'historical')
            hist = iris.load_cube(ano_hist)
            hist = utils.time_slicer(hist, 'historical')
            hist = hist.collapsed('year', iris.analysis.MEAN)

            data = utils.anomalies(hist, cube, percentage=False)
            data_perc = utils.anomalies(hist, cube, percentage=True)

            data = data.data
            data_perc = data_perc.data

            hhisto, bi = np.histogram(data, bins=np.linspace(data.min(), data.max(), 10))
            hhistop, bip = np.histogram(data_perc, bins=np.linspace(data_perc.min(), data_perc.max(), 10))

            an = 'anomaly'
            #ylabel = ' anomaly'
            ylabel = lblr.getYlab(metric, variable, anom="anomaly")

            an_p = 'percentageAnomaly'
            #ylabel_p = 'percentage anomaly'
            ylabel_p = lblr.getYlab(metric, variable, anom="percentageAnomaly")

            ldata.append((hhisto, bi))
            perc.append((hhistop, bip))

        else:
            cube = cube.data
            hhisto, bi = np.histogram(cube, bins=np.linspace(cube.min(), cube.max(), 10))
            ldata.append((hhisto, bi))
            #ylabel = vname
            ylabel = lblr.getYlab(metric, variable, anom="")
            an = 'scenarios'

        scen.append(fdict['scenario'])

        plot_dic1 = {'data': ldata,
                     'ftag': an,
                     'ylabel': ylabel,
                     }

        toplot = [plot_dic1]

        if anomaly:
            plot_dic2 = {'data': perc,
                         'ftag': an_p,
                         'ylabel': ylabel_p,

                         }

            toplot = [plot_dic1, plot_dic2]

    for p in toplot:

        if len(p['data']) < 4:
            xp = len(p['data'])
            yp = 1
            xx = 8
            yy = 9
        else:
            xp = 2
            yp = 2
            xx = 13
            yy = 8

        f = plt.figure(figsize=(xx, yy))

        for id in range(len(p['data'])):
            ax = f.add_subplot(xp, yp, id + 1)

            bin = p['data'][id][1]
            ax.bar(bin[0:-1] + ((bin[1::] - bin[0:-1]) / 2), p['data'][id][0], edgecolor='black',
                   width=(bin[1::] - bin[0:-1]),
                   align='edge', color='darkseagreen')

            ax.set_xlabel(p['ylabel']) #  + ': ' + fdict['metric']
            ax.set_ylabel('Number of models')
            #ax.set_title(scen[id])
            ax.set_title(lblr.getTitle(metric, variable, season, scenario, bc, region[1], anom=p['ftag']))

        plt.tight_layout()

        plt.savefig(outpath + os.sep + fdict['metric'] + '_' + fdict['variable'] + '_' +
                    fdict['bc_res'] + '_' + fdict['season'] + '_' + region[0] + '_MultiNbModelHistogram_' + p[
                        'ftag'] + '.png')

        plt.close(f)


def modelRank_scatter_single(incubes, outpath, region, anomaly=False):
    """
    Scatter plot showing the model ranks for a metric (anomaly) for a single scenario
   :param incubes: wildcard path to all tseries multi-model cubes
   :param outpath: the path where the plot is saved
   :param region: the region dictionary as defined in constants
   :param anomaly: boolean, switch for anomaly calculation
   :return: plot
   """
    ano = glob.glob(incubes + '_tseries.nc')
    if len(ano) != 1:
        sys.exit('Found too many files, need one file')
    ano = ano[0]

    fdict = utils.split_filename_path(ano)
    scen = fdict['scenario']
    metric = fdict['metric']
    variable = fdict['variable']
    season = fdict['season']
    bc = fdict['bc_res']

    if (anomaly == True) & (scen == 'historical'):
        return

    vname = cnst.VARNAMES[fdict['variable']]
    cube = iris.load_cube(ano)
    cube = utils.time_slicer(cube, fdict['scenario'])
    cube = cube.collapsed('year', iris.analysis.MEAN)

    if anomaly:
        ano_hist = ano.replace(fdict['scenario'], 'historical')
        hist = iris.load_cube(ano_hist)
        hist = utils.time_slicer(hist, 'historical')
        hist = hist.collapsed('year', iris.analysis.MEAN)

        data = utils.anomalies(hist, cube, percentage=False)
        data_perc = utils.anomalies(hist, cube, percentage=True)

        data = np.ndarray.tolist(data.data)
        data.sort()
        data_perc = np.ndarray.tolist(data_perc.data)
        data_perc.sort()

        plot_dic1 = {'data': data,
                     'ftag': scen + 'Anomaly',
                     'ylabel': lblr.getYlab(metric, variable, anom="anomaly"), #vname + ' anomaly: ' + fdict['metric'],
                     'minmax': utils.data_minmax(data)}

        plot_dic2 = {'data': data_perc,
                     'ftag': scen + 'PercentageAnomaly',
                     'ylabel': lblr.getYlab(metric, variable, anom="percentageAnomaly"), #vname + ' anomaly percentage: ' + fdict['metric'],
                     'minmax': utils.data_minmax(data_perc)
                     }

        toplot = [plot_dic1, plot_dic2]

    else:
        cube = cube.data
        cube = np.ndarray.tolist(cube)
        cube.sort()

        plot_dic1 = {'data': cube,
                     'ftag': scen,
                     'ylabel': lblr.getYlab(metric, variable, anom=""),
                     'minmax': utils.data_minmax(cube)
                     }

        toplot = [plot_dic1]

    for p in toplot:

        cm = plt.get_cmap('seismic')

        f = plt.figure(figsize=(9,9))
        for i in range(0, len(p['data'])):
            plt.scatter(i, p['data'][i], c=p['data'][i], vmin=p['minmax'][0], vmax=p['minmax'][1], cmap=cm,
                        edgecolors='k')

        plt.ylabel(p['ylabel'])
        plt.xlabel("Model Rank")
        #plt.title(region[1] + ': ' + scen)
        plt.title(lblr.getTitle(metric, variable, season, scen, bc, region[1], anom=p['ftag']))
        plt.tick_params(axis='x', which='both', bottom='off', top='off')
        plt.savefig(outpath + os.sep + fdict['metric'] + '_' + fdict['variable'] + '_' +
                    fdict['bc_res'] + '_' + fdict['season'] + '_' + region[0] + '_allModelRank_' + p['ftag'] + '.png')

        plt.close(f)


def lineplot_scenarios(incubes, outpath, region):
    """
    Line plot showing how the metric evolves over the years for all models and all scenarios combined
   :param incubes: wildcard path to all tseries multi-model cubes
   :param outpath: the path where the plot is saved
   :param region: the region dictionary as defined in constants
   :return: plot
   """
    ano_list = glob.glob(incubes + '_tseries.nc')
    ano_list = utils.order(ano_list)[::-1]

    f = plt.figure(figsize=(8, 5), dpi=300)
    ax = f.add_subplot(111)

    colors = ['gray', 'gold', 'green', 'mediumblue'][::-1]
    tag = cnst.SCENARIO[::-1]
    scenarios = []

    for ano, co, ta in zip(ano_list, colors, tag):

        fdict = utils.split_filename_path(ano)
        scen = fdict['scenario']
        metric = fdict['metric']
        variable = fdict['variable']
        season = fdict['season']
        bc = fdict['bc_res']
        scenarios.append(scen)

        cube = iris.load_cube(ano)
        time = cube.coord('year').points
        cube = cube.data

        ax.plot(time[0], 0, color=co, label=ta)
        for nb in range(cube.shape[0]):
            ax.plot(time, cube[nb, :], color=co, alpha=0.5, lw=0.75)

    bottom, top = ax.get_ylim()
    plt.vlines(2005, bottom, top, linestyle='--', linewidth=1.5, zorder=10)
    plt.ylabel(lblr.getYlab(metric, variable, anom=""))
    #plt.title(region[1])
    plt.title(lblr.getTitle(metric, variable, season, scenarios, bc, region[1], anom=''))
    plt.legend()
    plt.savefig(outpath + os.sep + fdict['metric'] + '_' + fdict['variable'] + '_' +
                fdict['bc_res'] + '_' + fdict['season'] + '_' + region[0] + '_lineplot_allscen_' + '.png')
    plt.close(f)
