import iris.plot as iplt
import iris.quickplot as qplt
import iris
import matplotlib.pyplot as plt
import numpy as np 

def timeseries(incube, plotpath, modelID):
    # Plot a timeseries for a smaller domain
    print 'plotting a timeseries'
    spi_cotedivoire = incube.intersection(latitude=(4,12), longitude=(-2,9))
    spi_ts = spi_cotedivoire.collapsed(['latitude', 'longitude'], iris.analysis.MEAN)
    qplt.plot(spi_ts)
    
    qplt.plot(spi_ts, label='spi', color='black', lw=1.5)
    plt.xlabel('Month')
    plt.ylabel('spi')
    plt.suptitle('Monthly Standardized Precipitation Index over CI', fontsize=16)
    #plt.show()
    plt.savefig(plotpath+'ts_'+modelID+'.png')
     
def map(incube, plotpath, modelID):
    # plot a map for a smaller domain
    print 'plotting a map'
    fig = plt.figure(figsize=(12, 5))
    qplt.contourf(incube[5,:,:])
                      
    plt.gca().coastlines()
#    # get the current axes' subplot for use later on
#    plt1_ax = plt.gca()
#
#    # Add the second subplot showing the A1B scenario
#    plt.subplot(122)
#    contour_result = iplt.contourf(spi_ts)
#                                    
#    # get the current axes' subplot for use later on
#    plt2_ax = plt.gca()ttom, width, height = plt2_ax.get_position().bounds
#    first_plot_left = plt1_ax.get_position().bounds[0]
#    colorbar_axes = fig.add_axes([first_plot_left, bottom + 0.07, width, 0.03])
    cbar = plt.colorbar(spi_ts, colorbar_axes, orientation='horizontal')
    plt.suptitle('Monthly distribution of the SPI over WA', fontsize=18)
    #plt.show()
    plt.savefig(plotpath+'ts_'+modelID+'.png')
