'''
master.py
created: December 2016
created by: Rory F
So, this is the new master script.
And you never need to touch it.
EVER.
If you do, Santa will know.

What this does, is take several different variables passed
in from ultimo_burrito and then create the metric netCDF files,
make a large cube of all metric values for all models,
and plot the whole thing.

But, in order to do this, it uses several variables from ultimo_burrito
that are quite sensitive.

For example, it will call a custom calc_ file depending on what
calc_ file is chosen in ultimo_burrito.

Hence why we ask you not to play with this.

'''

# First we load general functions that will always be used
import load_file_names  # loads all files of a certain form from a given inpath
import load_data  # loads and spatially slices the data for each file found by load_file_names
import make_big_cube  # Andy's baby
import iris  # loved and trusted since 1896


def master(variable, scenario, bc_and_resolution, inpath, outpath, season, region, calc_file, xmin, xmax, ymin, ymax,
           plotter, overwrite):  # All these variables are passed through from ultimo_burrito

    #    iris.FUTURE.netcdf_no_unlimiter=True
    for sc in scenario:
        for bc in bc_and_resolution:
            for seas in season:

                print inpath, sc, bc, seas
                files_good, modelID = load_file_names.load_file_names(inpath, variable, sc,
                                                                      bc)  # load all suitable files names and return a list with file names and another list with just
                # the model IDs

                if files_good == []:
                    print 'No files found. Please check you chose an input directory!'
                    return
                # now we load the calc file
                # this is done with the same __import__ trick shown in ultimo_burrito.py
                # By doing this, to calculate a different metric, we never have to change master
                # as master always runs a file called "calc_file_script"
                # what calc_file_script refers to is set by ultimo_burrito
                # so the master script just passes information from the burrito to the calc script.
                # But we want to keep the variable calc_file as it is, because this is the description of
                # the metric being calculated. We can use this as a title for the plots we produce, an
                # identifier that is easy to understand for netCDF files and many other wonderful things (calorie free chocolate maybe?)
                calc_file_load = 'calc_' + str(calc_file)
                calc_file_script = __import__(calc_file_load)

                for fle in files_good:  # loop through files found in the load_file_names
                    for nme in modelID:  # seperate loop here to set up the correct ncfile name
                        # this part of the code makes sure that we have the right modelID for the file we are using (it should only hit once)
                        # then make a unique identifier called ncfile that we can use to save the netcdf and never overwrite things we don't want to
                        if nme in fle:
                            nc_file = outpath + '/' + str(calc_file) + '_' + str(bc) + '_' + str(sc) + '_' + str(
                                seas) + '_' + str(region) + '_' + str(nme) + '.nc'
                            # we do another trick here, that we use for the make_big_cube code.
                            # Look at how nc_file is constructed.
                            # For all models, this name is going to be identical, until the bit where we add the string "nme", that is the unique modelID
                            # So, if I want a cube of all variables with the same metric, bias corrections settings, scenarion, season and region,
                            # I can split nc_file at nme, and return whatever comes before the model ID (nme)
                            # We do this every time, which is redundant, but it ensures it is done (also the time it takes is not time you will ever miss.
                            file_searcher = nc_file.split(str(nme))[0]
                    # next we try to open the nc_file.
                    # This stops us remaking a file that already exists.
                    # there will be a patch where this is overwritten by chosen to remake the metric output files (useful if you notice an error
                    # in your metric calculation file.
                    if overwrite == 'No':
                        try:
                            cubeout = iris.load(nc_file)
                        except IOError:  # if no file exists called nc_file...
                            print "No netCDF found, calculating anyway"
                            cubeout = load_data.load_data(fle, xmin, xmax, ymin,
                                                          ymax)  # ...load the data needed to make it
                            calc_file_script.main(cubeout, seas, nc_file)  # and make it
                    else:
                        #          	     print nc_file
                        cubeout = load_data.load_data(fle, xmin, xmax, ymin, ymax)  # ...load the data needed to make it
                        calc_file_script.main(cubeout, seas, nc_file)  # and make it


                    # makea big cube of all the files that look like file_searcher. Read make_big_cube for more details
                bigcube = make_big_cube.make_big_cube(file_searcher)

                # This is another custom import. They blow my tiny little mind.
                make_big_plot = __import__(plotter)

                # create a unique identifier for the plot made in make_big_plot (this will double up as the default plot title
                # if one is not given in the calc file
                what_am_i = str(calc_file) + '-' + str(bc) + '-' + str(sc) + '-' + str(seas) + '-' + str(region)
                # send bigcube to plotter, and save file what_am_i in the directory outpath
                make_big_plot.main(bigcube, outpath, what_am_i)


if __name__ == "__main__":
    master()
