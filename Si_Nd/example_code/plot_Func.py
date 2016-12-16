'''
plot_Func.py
This function make some plot
Author: Siny NDOYE, December 2016

'''

import os
import iris
import iris.quickplot as qplt
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as bm
#import pdb
#def plot_Func(cube2plot,outpath,mnth,nlevc):
def plot_Func(cube2plot,figpath,mnth,nlevc,xstart,xend,ystart,yend,title_name): 
#    pdb.set_trace()
#    print cube2plot.collapsed(['time', 'latitude','longitude'],iris.analysis.MIN), nlevc
    #levels = np.linspace(iris.analysis.MIN(cube2plot),iris.analysis.MAX(cube2plot) , nlevc)
    plt.clf()
    levels=np.linspace(282,302,nlevc)
    levels=np.linspace(8,32,nlevc)

    qplt.contourf(cube2plot, levels = levels, extend = 'max')
    m = bm.Basemap(projection='cyl', llcrnrlat=ystart, urcrnrlat=yend, llcrnrlon=xstart, urcrnrlon=xend, resolution='c')  # coarse resolution for grid
    #m = bm.Basemap(projection='cyl', llcrnrlat=8.0, urcrnrlat=16.0, llcrnrlon=-20.0, urcrnrlon=20.0, resolution='c')  # coarse resolution for grid
    
    m.drawcoastlines(linewidth=2)
    m.drawcountries(linewidth=1)
    plt.title(title_name)
    if not os.path.exists(figpath):
        os.makedirs(figpath)       
         
    plt.savefig(figpath +'Tmean'+str(mnth)+'.png' )
    plt.show()
    
    
#if __name__== '__main__':
#    plot_Func(cube2plot,outpath,mnth,nlevc)
    #plot_Func(cube2plot,outpath,mnth,nlevc,xstart,xend,ystart,yend) 