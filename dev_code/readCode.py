#!/usr/local/sci/bin/python2.7

import os, sys
import iris

def callback_champ_stdcal(cube, field, filename):
    '''
    What it does  : Modify cubes at read time to remove problematic metadata
            and unify time coordinates, eg. for /project/champ data
    How to use it : cubes=iris.load(filenames,variable,callback=callback_champ_stdcal)
    Who           : Andy Hartley, with help from Matt Mizielinski
    '''

    this_time_unit = cf_units.Unit("days since 1800-01-01", calendar=cube.coord('time').units.calendar)
    new_time_unit = cf_units.Unit('days since 1800-01-01', calendar='gregorian')

    for att in ['history', 'cmor_version', 'creation_date', 'references', 'mo_runid', 'tracking_id', 'table_id', 'forcing']:
        cube.attributes[att] = "overwritten"

    iris.coord_categorisation.add_month_number(cube, 'time', name='month_number')
    iris.coord_categorisation.add_year(cube, 'time', name='year')
    iris.coord_categorisation.add_season(cube, 'time', name='season')
    iris.coord_categorisation.add_season_year(cube, 'time', name='season_year')

    timepoints = []
    for y,m in zip(cube.coord('year').points, cube.coord('month_number').points):
        t = new_time_unit.date2num(datetime.datetime(int(y), int(m), 15, 0, 0))
        timepoints.append(t)

    newtimecoord = iris.coords.DimCoord(timepoints, 'time', units = new_time_unit)
    time_dims = cube.coord_dims('time')
    cube.remove_coord('time')
    cube.add_dim_coord(newtimecoord, time_dims)

def callback_champ_daily(cube, field, filename):
    '''
    What it does  : Modify cubes at read time to remove problematic metadata
            and unify time coordinates, eg. for /project/champ data
    How to use it : cubes=iris.load(filenames,variable,callback=callback_champ_stdcal)
    Who           : Andy Hartley, with help from Matt Mizielinski
    '''

    this_time_unit = cf_units.Unit("days since 1800-01-01", calendar=cube.coord('time').units.calendar)
    new_time_unit = cf_units.Unit('days since 1800-01-01', calendar='gregorian')

    for att in ['history', 'cmor_version', 'creation_date', 'references', 'mo_runid', 'tracking_id', 'table_id', 'forcing']:
        cube.attributes[att] = "overwritten"

    iris.coord_categorisation.add_day_of_month(cube, 'time', name='day_of_month')
    iris.coord_categorisation.add_month_number(cube, 'time', name='month_number')
    iris.coord_categorisation.add_year(cube, 'time', name='year')
    iris.coord_categorisation.add_season(cube, 'time', name='season')
    iris.coord_categorisation.add_season_year(cube, 'time', name='season_year')

    timepoints = []
    for y,m,d in zip(cube.coord('year').points, cube.coord('month_number').points, cube.coord('day_of_month').points):
        t = new_time_unit.date2num(datetime.datetime(int(y), int(m), int(d), 0, 0))
        timepoints.append(t)

    newtimecoord = iris.coords.DimCoord(timepoints, 'time', units = new_time_unit)
    time_dims = cube.coord_dims('time')
    cube.remove_coord('time')
    cube.add_dim_coord(newtimecoord, time_dims)

def getRegParams(reg):

    reg_params = { 'trop'     : [-30.0, 30.0, -180.0, 180.0, False],
                   'tropland' : [-30.0, 30.0, -180.0, 180.0, True],
                   'tropzoom' : [-20.0, 90.0, -120.0, 160.0, False],
                   'nae'      : [-30.0, 30.0, -180.0, 180.0, False],
                   'glo'     : [-90.0, 90.0, -180.0, 180.0, False],
                   'g_of_g'   : [-5.0, 5.0, -20.0, -5.0, True], # eastern equatorial Atlantic. Source: Janicot et al., 1998 http://dx.doi.org/10.1175/1520-0442-11.8.1874
                   'wafr'     : [-5.0, 30.0, -30.0, 35.0, False]}

    return(reg_params[reg])

    
def makeCmipCube(infiles, varname, fullvarname, minyear, maxyear, template):
    '''
    Makes a cube only from the relevant CMIP5 input files.
    This is useful because it removes problems that may occur with files that are outside the period of interest
    '''
    if '@' in varname:
        plev = int(varname.split('@')[1])
        var = varname.split('@')[0]
    else:
        plev = 'none'

    model_cubes = iris.cube.CubeList([])
    # Loop through files, and only use files that are <= maxfutureyear
    for file in infiles:
        # Use the file path to determine the start and end date of the data
        file_dates = os.path.splitext(os.path.basename(file))[0].split('_')[5]
        strt_dt_txt = file_dates.split('-')[0]
        end_dt_txt = file_dates.split('-')[1]
        strt_dt = datetime.datetime(int(strt_dt_txt[0:4]), int(strt_dt_txt[4:6]), 1, 0, 0)
        end_dt = datetime.datetime(int(end_dt_txt[0:4]), int(end_dt_txt[4:6]), 1, 0, 0)
        # If the start date is within the
        #print 'minyear: ' + str(minyear) + ', maxyear: ' + str(maxyear)
        if (strt_dt.year < maxyear) & (end_dt.year > minyear):
            #print file
            cube = iris.load_cube(file, fullvarname, callback=io.callback_champ_stdcal) # varname,
            # Extract correct vertical level
            if not plev == 'none':
                try:
                    cube = cube.extract(iris.Constraint(air_pressure=plev*100.))
                except:
                    try:
                        cube = cube.extract(iris.Constraint(atmosphere_hybrid_sigma_pressure_coordinate=plev*100.))
                    except:
                        print 'Probably need to change air_pressure for something else '
                        pdb.set_trace()

            model_cubes.append(cube)


    iris.util.unify_time_units(model_cubes)
    iris.experimental.equalise_cubes.equalise_attributes(model_cubes)

    # Equalise metadata ...
    for i in 1+np.arange(len(model_cubes)-1):
        model_cubes[i].metadata = model_cubes[0]

    try:
        model_cube = model_cubes.concatenate_cube()
    except:
        print 'Concatenation failed ...'
        pdb.set_trace()

    # Extract relevant years from the data
    yrcon = iris.Constraint(season_year = lambda cell, minyr=minyear, maxyr=maxyear: minyr <= cell <= maxyr)
    model_ss = model_cube.extract(yrcon)
    # Regrid to tempate grid
    model_ss = guesslatlonbounds(model_ss)
    model_ss = model_ss.regrid(template,ia.AreaWeighted())
    #print model_ss

    if varname == 'precipitation_flux':
        model_ss = proc.precip_to_mmpday(model_ss)

    return(model_ss)


def makeSeasCube(model_cube, seas):

    sncon = {'ann': iris.Constraint(month_number=lambda cell: 1 <= cell <= 12),
                  'mj' : iris.Constraint(month_number=lambda cell: 5 <= cell <= 6),
                  'jj' : iris.Constraint(month_number=lambda cell: 6 <= cell <= 7),
                  'ja' : iris.Constraint(month_number=lambda cell: 7 <= cell <= 8),
                  'as' : iris.Constraint(month_number=lambda cell: 8 <= cell <= 9),
                  'so' : iris.Constraint(month_number=lambda cell: 9 <= cell <= 10),
                  'jan' :  iris.Constraint(month_number=lambda cell: cell == 1),
                  'feb' :  iris.Constraint(month_number=lambda cell: cell == 2),
                  'mar' :  iris.Constraint(month_number=lambda cell: cell == 3),
                  'apr' :  iris.Constraint(month_number=lambda cell: cell == 4),
                  'may' :  iris.Constraint(month_number=lambda cell: cell == 5),
                  'jun' :  iris.Constraint(month_number=lambda cell: cell == 6),
                  'jul' :  iris.Constraint(month_number=lambda cell: cell == 7),
                  'aug' :  iris.Constraint(month_number=lambda cell: cell == 8),
                  'sep' :  iris.Constraint(month_number=lambda cell: cell == 9),
                  'oct' :  iris.Constraint(month_number=lambda cell: cell == 10),
                  'nov' :  iris.Constraint(month_number=lambda cell: cell == 11),
                  'dec' :  iris.Constraint(month_number=lambda cell: cell == 12),
                  'djf': iris.Constraint(month_number=lambda cell: (cell == 12) | (1 <= cell <= 2)),
                  'mam': iris.Constraint(month_number=lambda cell: 3 <= cell <= 5),
                  'jja': iris.Constraint(month_number=lambda cell: 6 <= cell <= 8),
                  'jas': iris.Constraint(month_number=lambda cell: 7 <= cell <= 9),
                  'son': iris.Constraint(month_number=lambda cell: 9 <= cell <= 11)
                  }

    scube = model_cube.extract(sncon[seas])
    outcube = scube.collapsed('time', iris.analysis.MEAN)

    return(outcube)

    
def main():

    model = 'ACCESS1-0'
    aseasons=['jas', 'mj', 'jj', 'ja', 'as', 'so']
    scenarios = ['rcp85','historical'] 
    variables = {'pr'  : 'precipitation_flux',
                 'psl' : 'air_pressure_at_sea_level',
                 'huss':'specific_humidity',
                 'tas' :'air_temperature',
                 'hurs':'relative_humidity'
                }

    
    minlat, maxlat, minlon, maxlon, applyseamask = getRegParams(reg)
    lonce = iris.coords.CoordExtent('longitude', minlon,maxlon)
    latce = iris.coords.CoordExtent('latitude', minlat, maxlat)

    model_cube = makeCmipCube(infiles, varname, get_full_varname(var), minyear, maxyear, template)
    
    for seas in aseasons:
        print reg + ' : ' + seas
        scube = makeSeasCube(model_cube, seas)
        reg_scube = scube.intersection(lonce, latce)
        if applyseamask:
            reg_landf = landfrac.intersection(lonce, latce)
            reg_landf.data = ma.masked_less(reg_landf.data, landthresh)
            seamask = reg_landf.data.mask
            reg_scube.data = ma.masked_where(seamask, reg_scube.data)
        outfile = scendir + varname + '_Clim' + str(minyear) + str(maxyear) + '_' + model + '_' + scen + '_r' + ens + 'i1p1_' + seas + '_' + reg + '.nc'
        if not os.path.isfile(outfile):
            print outfile
            iris.save(reg_scube, outfile)

if __name__ == '__main__':
    main()
