"""
This module contains all calculation functions for the climate metrics atlas

Every calc script must return a 2d cube (collapsed over time) and a 1d time series cube (collapsed over area). Based
on these two aggregations, all possible following anomaly calculations and plots can be handled.

C. Klein 2017
"""

import iris
import iris.coord_categorisation
import numpy as np
import constants as cnst
import pdb


def _getSeasConstr(name):
    """
    A few definitions for seasonal slicing

    :param name: string indicating the season
    :return: corresponding iris contraint to be used for extracting a seasonal time slice
    """

    sncon = {'ann': iris.Constraint(month_number=lambda cell: 1 <= cell <= 12),
             'mj': iris.Constraint(month_number=lambda cell: 5 <= cell <= 6),
             'jj': iris.Constraint(month_number=lambda cell: 6 <= cell <= 7),
             'ja': iris.Constraint(month_number=lambda cell: 7 <= cell <= 8),
             'as': iris.Constraint(month_number=lambda cell: 8 <= cell <= 9),
             'so': iris.Constraint(month_number=lambda cell: 9 <= cell <= 10),
             'jan': iris.Constraint(month_number=lambda cell: cell == 1),
             'feb': iris.Constraint(month_number=lambda cell: cell == 2),
             'mar': iris.Constraint(month_number=lambda cell: cell == 3),
             'apr': iris.Constraint(month_number=lambda cell: cell == 4),
             'may': iris.Constraint(month_number=lambda cell: cell == 5),
             'jun': iris.Constraint(month_number=lambda cell: cell == 6),
             'jul': iris.Constraint(month_number=lambda cell: cell == 7),
             'aug': iris.Constraint(month_number=lambda cell: cell == 8),
             'sep': iris.Constraint(month_number=lambda cell: cell == 9),
             'oct': iris.Constraint(month_number=lambda cell: cell == 10),
             'nov': iris.Constraint(month_number=lambda cell: cell == 11),
             'dec': iris.Constraint(month_number=lambda cell: cell == 12),
             'djf': iris.Constraint(month_number=lambda cell: (cell == 12) | (1 <= cell <= 2)),
             'mam': iris.Constraint(month_number=lambda cell: 3 <= cell <= 5),
             'jja': iris.Constraint(month_number=lambda cell: 6 <= cell <= 8),
             'jas': iris.Constraint(month_number=lambda cell: 7 <= cell <= 9),
             'jjas': iris.Constraint(month_number=lambda cell: 6 <= cell <= 9),
             'mjjas': iris.Constraint(month_number=lambda cell: 5 <= cell <= 9),
             'son': iris.Constraint(month_number=lambda cell: 9 <= cell <= 11)
             }

    return (sncon[name])


def annualMax(cubein, season, ncfile):
    '''
    Calculates the annual maximum of a variable.

    :param incube: single variable cube from CMIP5 raw data
    :param season: string indicating season, read by _getSeasConstr() to get season contraint
    :param ncfile: full string for output netcdf file
    :return: single model netcdf file
    '''

    print ncfile
    print 'Calculating annual maximum'

    iris.coord_categorisation.add_year(cubein, 'time', name='year')
    iris.coord_categorisation.add_month_number(cubein, 'time', name='month_number')

    slicer = _getSeasConstr(season)
    cubein = cubein.extract(slicer)

    cube2plot = cubein
    if "pr_" in ncfile:
        cube2plot.convert_units('kg m-2 day-1')

    if ("tas_" in ncfile) or ('tasmax_' in ncfile) or ('tasmin_' in ncfile):
        cube2plot.convert_units('Celsius')

    calc = cube2plot.aggregated_by(['year'], iris.analysis.MAX)
    tseries = calc.collapsed(['longitude','latitude'], iris.analysis.MEAN)
    c2d = calc.collapsed('year', iris.analysis.MEAN)

    nc2d = ncfile.replace(cnst.AGGREGATION[0], cnst.AGGREGATION[1])

    iris.save(tseries, ncfile)
    iris.save(c2d, nc2d)


def annualMin(cubein, season, ncfile):
    '''
    Calculates the annual minimum of the variable.

    :param incube: single variable cube from CMIP5 raw data
    :param season: string indicating season, read by _getSeasConstr() to get season contraint
    :param ncfile: full string for output netcdf file
    :return: single model netcdf file
    '''

    print ncfile
    print 'Calculating annual minimum'

    iris.coord_categorisation.add_year(cubein, 'time', name='year')
    iris.coord_categorisation.add_month_number(cubein, 'time', name='month_number')

    slicer = _getSeasConstr(season)
    cubein = cubein.extract(slicer)

    cube2plot = cubein
    if "pr_" in ncfile:
        cube2plot.convert_units('kg m-2 day-1')

    if ("tas_" in ncfile) or ('tasmax_' in ncfile) or ('tasmin_' in ncfile):
        cube2plot.convert_units('Celsius')

    calc = cube2plot.aggregated_by(['year'], iris.analysis.MIN)
    tseries = calc.collapsed(['longitude', 'latitude'], iris.analysis.MEAN)
    c2d = calc.collapsed('year', iris.analysis.MEAN)

    nc2d = ncfile.replace(cnst.AGGREGATION[0], cnst.AGGREGATION[1])
    iris.save(tseries, ncfile)
    iris.save(c2d, nc2d)


def annualTotalRain(incube, season, ncfile):
    '''
    Calculates the total rain over the time period

    :param incube: precipitation cube from CMIP5 raw data
    :param season: string indicating season, read by _getSeasConstr() to get season contraint
    :param ncfile: full string for output netcdf file
    :return: single model netcdf file
    '''

    print ncfile
    print 'Calculating total rain'

    slicer = _getSeasConstr(season)
    iris.coord_categorisation.add_month_number(incube, 'time', name='month_number')
    iris.coord_categorisation.add_year(incube, 'time', name='year')

    incube = incube.extract(slicer)
    incube.convert_units('kg m-2 day-1')

    calc = incube.aggregated_by(['year'], iris.analysis.SUM)
    tseries = calc.collapsed(['longitude', 'latitude'], iris.analysis.MEAN)
    c2d = calc.collapsed('year', iris.analysis.MEAN)

    nc2d = ncfile.replace(cnst.AGGREGATION[0], cnst.AGGREGATION[1])
    iris.save(tseries, ncfile)
    iris.save(c2d, nc2d)


def annualMean(incube, season, ncfile):
    '''
    Calculates the annual mean over the time period

    TODO: allow lower threshold to compute mean based on e.g. RAINY days rather than all days

    :param incube: single variable cube from CMIP5 raw data
    :param season: string indicating season, read by _getSeasConstr() to get season contraint
    :param ncfile: full string for output netcdf file
    :return: single model netcdf file
    '''

    print ncfile
    print 'Calculating annual mean'

    slicer = _getSeasConstr(season)
    iris.coord_categorisation.add_year(incube, 'time', name='year')
    iris.coord_categorisation.add_month_number(incube, 'time', name='month_number')

    incube = incube.extract(slicer)
    cube2plot = incube

    if "pr_" in ncfile:
        cube2plot.convert_units('kg m-2 day-1')

    if ("tas_" in ncfile) or ('tasmax_' in ncfile) or ('tasmin_' in ncfile):
        cube2plot.convert_units('Celsius')

        calc = incube.aggregated_by(['year'], iris.analysis.MEAN)
    tseries = calc.collapsed(['longitude', 'latitude'], iris.analysis.MEAN)
    c2d = calc.collapsed('year', iris.analysis.MEAN)

    nc2d = ncfile.replace(cnst.AGGREGATION[0], cnst.AGGREGATION[1])
    iris.save(tseries, ncfile)
    iris.save(c2d, nc2d)


def monthlyClimatologicalMean(incube, season, ncfile):
    '''
    Calculates the climatological monthly means over the time period

    TODO: allow lower threshold to compute mean based on e.g. RAINY days rather than all days

    :param incube: single variable cube from CMIP5 raw data
    :param season: string indicating season, read by _getSeasConstr() to get season contraint
    :param ncfile: full string for output netcdf file
    :return: single model netcdf file
    '''

    print ncfile
    print 'Calculating climatological monthly mean'

    iris.coord_categorisation.add_month_number(incube, 'time', name='month_number')

    slicer = _getSeasConstr(season)
    cubein = incube.extract(slicer)

    cube2plot = incube

    if "pr_" in ncfile:
        cube2plot.convert_units('kg m-2 day-1')

    if ("tas_" in ncfile) or ('tasmax_' in ncfile) or ('tasmin_' in ncfile):
        cube2plot.convert_units('Celsius')

    calc = cube2plot.aggregated_by('month_number', iris.analysis.MEAN)
    tseries = calc.collapsed(['longitude', 'latitude'], iris.analysis.MEAN)
    c2d = calc.collapsed('year', iris.analysis.MEAN)

    nc2d = ncfile.replace(cnst.AGGREGATION[0], cnst.AGGREGATION[1])
    iris.save(tseries, ncfile)
    iris.save(c2d, nc2d)


def AnnualnbDayPerc(incube, season, ncfile, upper_threshold=None, lower_threshold=None):
    '''
    Calculate percentage of days per year with higher value than threshold.
    Choose thresholds as needed e.g. 30mm for extreme and 1mm for rainy day.

    TODO: allow lower threshold to compute number of days based on e.g. RAINY days rather than all days
    Problem: Regional collapsing is done later but the average of the mean per pixel is not the same as
    the average collapsed over the region if sample size changes per pixel (e.g. with rainy days baseline)

    :param incube: precipitation cube from CMIP5 raw data
    :param season: string indicating season, read by _getSeasConstr() to get season contraint
    :param ncfile: full string for output netcdf file
    :param upper_threshold: threshold (>=) defining the value to be exceeded (e.g. extreme value or rainy day value
    :param lower_threshold: threshold (>=) defining the minimum value of valid pixels (eg. 0 or 0.1 or 1)
    :return: single model netcdf file
    '''
    if not upper_threshold:
        "No threshold given, please provide upper threshold, stopping calculation"

    print ncfile
    print "Calculating percentage of days with variable above " + str(upper_threshold)

    iris.coord_categorisation.add_month_number(incube, 'time', name='month_number')
    iris.coord_categorisation.add_year(incube, 'time', name='year')

    slicer = _getSeasConstr(season)
    cube2plot = incube.extract(slicer)
    cube2plot.coord('latitude').guess_bounds()
    cube2plot.coord('longitude').guess_bounds()
    if "pr_" in ncfile:
        cube2plot.convert_units('kg m-2 day-1')

    if ("tas_" in ncfile) or ('tasmax_' in ncfile) or ('tasmin_' in ncfile):
        cube2plot.convert_units('Celsius')

    bigger = cube2plot.aggregated_by('year', iris.analysis.COUNT, function=lambda values: values >= upper_threshold)
    monthcount = cube2plot.aggregated_by('year', iris.analysis.COUNT, function=lambda values: values >= lower_threshold)
    bigger.data = bigger.data.astype(float)
    monthcount.data = monthcount.data.astype(float)

    bigger_tseries = bigger.collapsed(['longitude', 'latitude'], iris.analysis.SUM)
    bigger_c2d = bigger.collapsed('year', iris.analysis.SUM)

    monthcount_tseries = monthcount.collapsed(['longitude', 'latitude'], iris.analysis.SUM)
    monthcount_c2d = monthcount.collapsed('year', iris.analysis.SUM)

    tseries = (bigger_tseries / monthcount_tseries) *100
    c2d = (bigger_c2d / monthcount_c2d) *100

    nc2d = ncfile.replace(cnst.AGGREGATION[0], cnst.AGGREGATION[1])
    iris.save(tseries, ncfile)
    iris.save(c2d, nc2d)

def AnnualHotDaysPerc(incube, season, ncfile):
    AnnualnbDayPerc(incube, season, ncfile, upper_threshold=40, lower_threshold=-50)


def AnnualRainyDaysPerc(incube, season, ncfile):
    AnnualnbDayPerc(incube, season, ncfile, upper_threshold=1, lower_threshold=0)

def AnnualRainyDaysPerc50(incube, season, ncfile):
    AnnualnbDayPerc(incube, season, ncfile, upper_threshold=50, lower_threshold=1)


def AnnualnbDay(incube, season, ncfile, threshold=None):
    '''
    Calculate number of days per year with higher value than threshold.
    Choose threshold as needed e.g. 30mm for extreme and 1mm for rainy day.

    :param incube: precipitation cube from CMIP5 raw data
    :param season: string indicating season, read by _getSeasConstr() to get season contraint
    :param ncfile: full string for output netcdf file
    :return: single model netcdf file
    '''
    if not threshold:
        print('No threshold given, stopping calculation')
        return

    print ncfile
    print "Calculating number of days with variable above " + str(threshold)

    iris.coord_categorisation.add_month_number(incube, 'time', name='month_number')
    iris.coord_categorisation.add_year(incube, 'time', name='year')

    slicer = _getSeasConstr(season)
    cube2plot = incube.extract(slicer)
    cube2plot.coord('latitude').guess_bounds()
    cube2plot.coord('longitude').guess_bounds()
    if "pr_" in ncfile:
        cube2plot.convert_units('kg m-2 day-1')

    if ("tas_" in ncfile) or ('tasmax_' in ncfile) or ('tasmin_' in ncfile):
        cube2plot.convert_units('Celsius')

    bigger = cube2plot.aggregated_by('year', iris.analysis.COUNT, function=lambda values: values >= threshold)
    bigger.data = bigger.data.astype(float)

    tseries = bigger.collapsed(['longitude', 'latitude'], iris.analysis.MEAN)
    c2d = bigger.collapsed('year', iris.analysis.MEAN)

    nc2d = ncfile.replace(cnst.AGGREGATION[0], cnst.AGGREGATION[1])
    iris.save(tseries, ncfile)
    iris.save(c2d, nc2d)

def AnnualHotDays(incube, season, ncfile):
    AnnualnbDay(incube, season, ncfile, threshold=40)

def AnnualExtremeRain50(incube, season, ncfile):
    AnnualnbDay(incube, season, ncfile, threshold=50)

def AnnualExtremeRain100(incube, season, ncfile):
    AnnualnbDay(incube, season, ncfile, threshold=100)

def SPIxMonthly(incube, season, ncfile):
    """
    Calculate SPI for given period up to one year.
    The SPI is the anomaly with respect to the chosen scenario baseline period.
    period - climatological_mean / climatological_std

    :param incube: precipitation cube from CMIP5 raw data
    :param season: string indicating season, read by _getSeasConstr() to get season contraint
    :param ncfile: full string for output netcdf file
    :return: single model netcdf file
    """

    print 'Calculating SPI for ' + str(season)

    iris.coord_categorisation.add_month_number(incube, 'time', name='month_number')
    iris.coord_categorisation.add_year(incube, 'time', name='year')
    slicer = _getSeasConstr(season)

    incube = incube.extract(slicer)

    c_monthly = incube.aggregated_by(['year'], iris.analysis.MEAN)
    c_monthly.convert_units('kg m-2 day-1')

    # This is the monthly climatology (mean and std deviation)
    std = c_monthly.collapsed('year', iris.analysis.STD_DEV)
    mean = c_monthly.collapsed('year', iris.analysis.MEAN)

    # We need to change the shape of the monthly climatologies to match the shape of the timeseries (in the cube c_monthly)
    mean = mean.data
    std = std.data

    clim_mean_data = np.repeat(mean.reshape(1, mean.shape[0], mean.shape[1]), c_monthly.shape[0],
                               axis=0)  # np.tile(mean.data, (c_monthly.shape[0] / mean.shape[0], 1, 1))
    clim_std_data = np.repeat(std.reshape(1, std.shape[0], std.shape[1]), c_monthly.shape[0],
                              axis=0)  # np.tile(std.data, (c_monthly.shape[0] / std.shape[0], 1, 1))

    clim_mean_cube = c_monthly.copy(clim_mean_data)
    clim_std_cube = c_monthly.copy(clim_std_data)

    spi = (c_monthly - clim_mean_cube) / clim_std_cube

    iris.save(spi, ncfile)


def onsetMarteau(incube, season, ncfile):
    """
    Calculate Marteau monsoon onset. Season is fixed to onset period

    :param incube: precipitation cube from CMIP5 raw data
    :param ncfile: full string for output netcdf file
    :return: single model netcdf file
    """

    season = 'mjjas'

    iris.coord_categorisation.add_month_number(incube, 'time', name='month_number')
    iris.coord_categorisation.add_year(incube, 'time', name='year')
    iris.coord_categorisation.add_day_of_year(incube, 'time', name='day_of_year')
    slicer = _getSeasConstr(season)
    cubein = incube.extract(slicer)

    cube2plot = cubein
    cube2plot.convert_units('kg m-2 day-1')

    yrs = cube2plot.aggregated_by('year', iris.analysis.MEAN)
    empty = yrs.data
    years = yrs.coord('year').points
    dates = []
    tester = 14
    onsets = np.zeros((empty.shape[0], empty.shape[1], empty.shape[2]), float)

    for yr in years:
        yrslice = iris.Constraint(year=lambda cell: cell == yr)
        holdr = cubein.extract(yrslice)
        strt_date = holdr.coord('day_of_year').points[0]
        holdr = holdr.data
        for x in range(0, holdr.shape[2]):
            for y in range(0, holdr.shape[1]):
                latmean = 0
                cnt0 = 0
                A = 0
                B = 0
                C = 0
                for t in xrange(0, holdr.shape[0] - tester - 6):
                    if holdr[t, y, x] > 1.0:
                        A4 = 1
                    else:
                        A4 = 0
                    if holdr[t + 1, y, x] + holdr[t, y, x] > 20.0:
                        A1 = 1
                    else:
                        A1 = 0
                    A2 = 1
                    t2 = 2
                    while t2 < tester - 6:
                        drytest = holdr[t + t2, y, x] + holdr[t + t2 + 1, y, x] + holdr[t + t2 + 2, y, x] + holdr[
                            t + t2 + 3, y, x] + holdr[t + t2 + 4, y, x] + holdr[t + t2 + 5, y, x] + holdr[
                                      t + t2 + 6, y, x]
                        if drytest < 5.0:
                            A2 = 0
                            break
                        else:
                            t2 = t2 + 1
                    A3 = A4 + A2 + A1
                    if A3 == 3:
                        latmean = t + strt_date

                        onsets[yr - years[0], y, x] = latmean

                        break
                    else:
                        continue
                    break
                if latmean == 0:
                    onsets[yr - years[0], y, x] = float('NaN')

    yrs.data = onsets[:]

    tseries = yrs.collapsed(['longitude', 'latitude'], iris.analysis.MEDIAN)
    c2d = yrs.collapsed('year', iris.analysis.MEDIAN)

    nc2d = ncfile.replace(cnst.AGGREGATION[0], cnst.AGGREGATION[1])
    iris.save(tseries, ncfile)
    iris.save(c2d, nc2d)
