'''
'''


import iris
import scipy.stats as stat
from numpy import genfromtxt as gent
import matplotlib.pyplot as plt
import glob
import numpy as np

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
            '26': 'green'
            }

    return(sncon[name])

def get_line_style(name):


    sncon = {'0': '*',
            '1' : 's',
            '2' : '^',
            '3' : '*',
            '4' : 's',
            '5' : '^',
            '6' : '*',
            '7' : 's',
            '8' : '^',
            '9' : '*',
            '10' : 's',
            '11' : '^',
            '12' : '*',
            '13' : 's',
            '14' : '^',
            '15' : '*',
            '16' : 's',
            '17' : '^',
            '18': '*',
            '19': 's',
            '20': '^',
            '21': 'D',
            '22': 'D',
            '23': 'D',
            '24': 'D',
            '25': 'D',
            '26': 'D'
            }

    return(sncon[name])









def main(incube,outpath,what_am_i):
    plt.clf()
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



    plt.clf()
# First we do the postage stamps
    plt.figure(figsize = (16,16))
    cntr = 0
    for t in modelnums:
        plt.subplot(6,5,cntr+1)
        slicer = iris.Constraint(model_name = str(t))
        range_finder = incube.extract(slicer)
        range_finder = range_finder.data
        color = get_color(str(cntr))
        line_style = get_line_style(str(cntr))
	print range_finder.shape, len(times)
        plt.scatter(times[:],range_finder[:],marker = line_style,c=color, label = t)
        plt.title(str(t))
	plt.xlim(times[0] - 1, times[-1] +1)
	cntr = cntr + 1
# need to find out how to grab the units of the cube from the cube
    plt.suptitle(str(what_am_i))
    plt.savefig(str(outpath)+'/'+str(what_am_i)+'_postage_stamps.png')


# then we add everyone to the same plot
    plt.clf()
    plt.figure(figsize = (16,16))
    cntr = 0
    for t in modelnums:
        slicer = iris.Constraint(model_name = str(t))
        range_finder = incube.extract(slicer)
        range_finder = range_finder.data
        color = get_color(str(cntr))
        line_style = get_line_style(str(cntr))
        plt.scatter(times[:],range_finder[:],marker = line_style,c=color, label = t)
	cntr = cntr + 1
# need to find out how to grab the units of the cube from the cube 
    plt.xlim(times[0] - 1, times[-1]+10)
    plt.legend(loc = 'best')
    plt.suptitle(str(what_am_i))
    plt.savefig(str(outpath)+'/'+str(what_am_i)+'all_in_one.png')
    plt.show()




if __name__ == "__main__":
	scatter(incube,outpath,what_am_i)
