
import load_file_names  # loads all files of a certain form from a given inpath
import load_data  # loads and spatially slices the data for each file found by load_file_names
import make_big_cube  # Andy's baby
import iris  # loved and trusted since 1896
import make_big_anomaly

def run(variable, scenario, bc_and_resolution, inpath, outpath, season, region, calc_file, xmin, xmax, ymin, ymax,
           plotter, overwrite):

    iris.FUTURE.netcdf_no_unlimiter=True
    for sc in scenario:
        for bc in bc_and_resolution:
            for seas in season:

                print inpath, sc, bc, seas
                files_good, modelID = load_file_names.load_file_names(inpath, variable, sc, bc)
                # the model IDs

                if files_good == []:
                    print 'No files found. Please check you chose an input directory!'
                    return

                calc_file_load = 'calc_' + str(calc_file)
                calc_file_script = __import__(calc_file_load)

                for fle in files_good:
                    for nme in modelID:
                        if nme in fle:
                            nc_file = outpath + '/' + str(calc_file) + '_' + str(bc) + '_' + str(sc) + '_' + str(
                                seas) + '_' + str(region) + '_' + str(nme) + '.nc'

                            file_searcher = nc_file.split(str(nme))[0]

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



                try:
			bigcube = iris.load_cube(str(file_searcher)+'_all_models.nc')
		except IOError: 
	                bigcube = make_big_cube.make_big_cube(file_searcher)
		else:
			bigcube = iris.load_cube(str(file_searcher)+'_all_models.nc')
                # This is another custom import. They blow my tiny little mind.
                #print bigcube
                make_big_plot = __import__(plotter)


                what_am_i = str(calc_file) + '-' + str(bc) + '-' + str(sc) + '-' + str(seas) + '-' + str(region)
                # send bigcube to plotter, and save file what_am_i in the directory outpath
                make_big_plot.main(bigcube, outpath, what_am_i,sc,file_searcher)


if __name__ == "__main__":
    master()
