import iris
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as bm
import numpy as np
import make_big_anomaly_percentage


def main(incube, outpath, what_am_i, sc, file_searcher):
    histcube_name = file_searcher.replace(sc, 'historical')
    try:
        histcube = iris.load_cube(str(histcube_name) + '_all_models.nc')
    except IOError:
        print 'One or more files do not exist. Exiting Code'
    else:

        cube2use = make_big_anomaly_percentage.main(incube, file_searcher, sc)
        print cube2use.data.shape

        while len(cube2use.coord('longitude').points) != 1:
            print len(cube2use.coord('longitude').points)
            print 'you want 1d DATA! Please type "y" on the command line when prompted'
            cube2use = make_big_anomaly_percentage.main(incube, file_searcher, sc)

        plt.clf()
        cube2plot = cube2use.data
        cube2plot = np.ndarray.tolist(cube2plot)
        cube2plot.sort()
        print cube2plot
        cm = plt.get_cmap('seismic')
        if np.abs(cube2plot[0]) < np.abs(cube2plot[-1]):
            vmi = np.abs(cube2plot[-1]) * -1
            vma = np.abs(cube2plot[-1])
        else:
            vmi = np.abs(cube2plot[0]) * -1
            vma = np.abs(cube2plot[0])
        for i in range(0, len(cube2plot)):
            plt.scatter(i, cube2plot[i], c=cube2plot[i], vmin=vmi, vmax=vma, cmap=cm)
        ylab = raw_input("Please enter y variable (e.g. change in your metric)")
        plt.ylabel(ylab)
        plt.xlabel("Model rank")
        plt.tick_params(acis='x', whcih='both', bottom='off', top='off')
        plt.savefig(str(what_am_i) + '_all_model_perc_scatter_difference.png')
        plt.show()


if __name__ == "__main__":
    main(incube, outpath, what_am_i)
