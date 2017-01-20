import iris
import scipy.stats as stat
from numpy import genfromtxt as gent
import matplotlib.pyplot as plt
import glob
import numpy as np
import ipdb

def get_color(name):

    sncon = {'0': 'k',
            '1' : 'k',
            '2' : 'k',
            '3' : 'r',
            '4' : 'r',
            '5' : 'r',
            '6' : 'b',
            '7' : 'b',
            '8' : 'b',
            '9' : 'y',
            '10' : 'y',
            '11' : 'y',
            '12' : 'purple',
            '13' : 'purple',
            '14' : 'purple',
            '15' : 'green',
            '16' : 'green',
            '17' : 'green',
            '18': 'pink',
            '19': 'pink',
            '20': 'pink',
            '21': 'k',
            '22': 'r',
            '23': 'b',
            '24': 'y',
            '25': 'purple',
            '26': 'green',	
	    '27': 'k',
            '28': 'r',
            '29': 'b',
            '30': 'y'   }

    return(sncon[name])


def main(incube,outpath,what_am_i):
    ranger = 0
    low = 0
    high = 0
    times = incube.coord('year').points
    modelnums = incube.coord('model_name').points


    for t in modelnums:
        slicer = iris.Constraint(model_name = str(t))
        range_finder = incube.extract(slicer)
        range_finder = range_finder.data
        ranger_test = np.max(range_finder[:]) - np.min(range_finder[:])
        if ranger_test > ranger:
            ranger = ranger_test
            low = np.min(range_finder[:])
	    high = np.max(range_finder[:])

# First we do the postage stamps
    plt.figure(figsize = (20,10))
    cntr = 0
    for t in modelnums:
        plt.subplot(5,6,cntr+1)
        slicer = iris.Constraint(model_name = str(t))
        range_finder = incube.extract(slicer)
        range_finder = range_finder.data
        color = get_color(str(cntr))	
        print range_finder.shape, len(times)
        plt.bar(times[:],range_finder[:],width=1,color=color, label = t)
        plt.title(str(t))
        plt.ylim(-3,3)
	plt.xlim(times[0] - 1, times[-1] +1)
	cntr = cntr + 1
# need to find out how to grab the units of the cube from the cube
    plt.suptitle(str(what_am_i))
    plt.tight_layout()
    plt.subplots_adjust(top=0.91)
    plt.savefig(str(outpath)+'/'+str(what_am_i)+'_postage_stamps.png')
    plt.show()

 # multimodel average
    plt.figure(figsize = (10,5))


    multimodel = incube.collapsed('model_name', iris.analysis.MEAN)


    plt.bar(times[:],multimodel.data[:],color='red', label = 'Multimodel mean')

# need to find out how to grab the units of the cube from the cube
    plt.xlim(times[0] - 1, times[-1]+10)
    plt.legend(loc = 'best')
    plt.title(str(what_am_i))
    plt.tight_layout()

    plt.savefig(str(outpath)+'/'+str(what_am_i)+'all_in_one.png')
    plt.show()


if __name__ == "__main__":
	line_plot_year(incube,outpath,what_am_i)
