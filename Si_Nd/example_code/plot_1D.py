'''
plot_1D.py
This function make some plot
Author: Siny NDOYE, December 2016

'''

import os
import iris
import iris.plot as iplt
#import iris.quickplot as qplt
#import numpy as np
import matplotlib.pyplot as plt
#import mpl_toolkits.basemap as bm
#import pdb
#def plot_Func(cube2plot,outpath,mnth,nlevc):
def plot_1D(cube2plot,figpath): 
    plt.clf()

    iplt.plot(cube2plot)
    #plt.title(title_name)
    if not os.path.exists(figpath):
        os.makedirs(figpath)       
         
    plt.savefig(figpath +'Ts.png' )
    plt.show()
    
    
#if __name__== '__main__':
#    plot_Func(cube2plot,outpath,mnth,nlevc)
    #plot_Func(cube2plot,outpath,mnth,nlevc,xstart,xend,ystart,yend) 