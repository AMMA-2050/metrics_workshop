#import iris.quickplot as qplt
#import numpy as np
import os
import iris
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import iris.plot as iplt
#import mpl_toolkits.basemap as bm
#import pdb
#def plot_Func(cube2plot,outpath,mnth,nlevc):
def plot_Tfilter(cube1plot,cube1plot24,cube1plot84,figpath):
    plt.clf()
    plt.figure(figsize=(9, 4))
    iplt.plot(cube1plot, color='0.7', linewidth=1., linestyle='-',
              alpha=1., label='no filter')
    iplt.plot(cube1plot24, color='b', linewidth=2., linestyle='-',
              alpha=.7, label='2-year filter')
    iplt.plot(cube1plot84, color='r', linewidth=2., linestyle='-',
              alpha=.7, label='7-year filter')
    plt.ylim([283, 303])
    #plt.title('Southern Oscillation Index (Darwin Only)')
    plt.xlabel('Time')
    plt.ylabel('Tas')
    plt.legend(fontsize=10)
    if not os.path.exists(figpath):
        os.makedirs(figpath)       
         
    
    plt.savefig(figpath +'Tf.png' )
    iplt.show()