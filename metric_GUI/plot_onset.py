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









def onset_plot(outpath):

    list_of_files = glob.glob(outpath+'/*onset_dates.csv')
    model_names = [f.split('/')[-1].split('_')[3] for f in list_of_files]
    plt.clf()
    plt.figure(figsize = (16,16))
    for file in list_of_files:
	holder = gent(file,delimiter = ',')
        fi = list_of_files.index(file)
        date_file = glob.glob(outpath+'/*years.csv')
        times = gent(date_file[fi],delimiter = ',')
        #times = np.arange(holder.shape[0])	
        print len(times), len(holder)
        color = get_color(str(fi))
        line_style = get_line_style(str(fi))
        plt.scatter(times,holder,marker = line_style,c=color, label = model_names[fi])
    plt.ylim(145,260)
    plt.xlim(times[0],times[-1]+15)
    plt.yticks([150,180,210,241],['1 June','1 July','1 Aug','1 Sep'])
#        plt.xticks([0,10,20,30,40,50],['1950','1960','1970','1980','1990','2000']) 
    plt.legend(loc = 'best')
    plt.savefig(outpath+'/SJ_onsets_all_models_scatter_hitorical.png')
    plt.show()







if __name__ == "__main__":
	onset_plot(outpath)
