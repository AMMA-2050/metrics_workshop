#######################
#
# workshop_contour_example_basemap.py
#
######################
import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt as gent
import mpl_toolkits.basemap as bm
from matplotlib import cm

### This plot could take a while! So be patient :)

def workshop_contour_example_basemap():
    # Read the data, adapt this path to your path if necessary
    mydata = gent('/nfs/see-fs-01_teaching/earv056/metrics_workshop/example_code/TRMM_v7_Marteau_onsets_1998_dry_spell_30.csv',
                  delimiter=',')

    # Shape of the data
    print(mydata.shape)

    ltd = np.linspace(-20, 20, 160)
    lat = np.linspace(8.0, 16.0, 32)
    levs = [119, 129, 139, 149, 159, 169, 179, 189, 200, 210, 220, 230, 240]

    # Open figure window
    ax1 = plt.figure(figsize=(10, 15))

    # Add first subplot
    plt.subplot(3, 1, 1)

    fig1 = plt.contour(ltd, lat, mydata[:], levs)
    plt.clabel(fig1, inline=1)   #adds numbers to your contours
    m = bm.Basemap(projection='cyl', llcrnrlat=8.0, urcrnrlat=16.0, llcrnrlon=-20.0, urcrnrlon=20.0, resolution='c')  # coarse resolution for grid
    m.drawcoastlines(linewidth=2)
    m.drawcountries(linewidth=1)
    plt.text(-21.5, 15, '(a)')

    # Add second subplot
    plt.subplot(3, 1, 2)
    fig2 = plt.contourf(ltd, lat, mydata[:], levs)
    m = bm.Basemap(projection='cyl', llcrnrlat=8.0, urcrnrlat=16.0, llcrnrlon=-20.0, urcrnrlon=20.0, resolution='l') # medium resolution for grid
    m.drawcoastlines(linewidth=2)
    m.drawcountries(linewidth=1)
    plt.text(-21.5, 15, '(b)')
    plt2_ax = ax1.gca()
    left0, bottom0, width0, height0 = plt2_ax.get_position().bounds
    cbar_1_ax = ax1.add_axes([left0, bottom0 - 0.01, width0, 0.015])
    cb2 = ax1.colorbar(fig2, cax=cbar_1_ax, orientation='horizontal')
    cb2.set_label('Marteau local onset 1998')

    # Add third subplot
    plt.subplot(3, 1, 3)
    my_pallet = cm.spectral
    my_pallet.set_over('w')
    my_pallet.set_under('w')
    my_pallet.set_bad(alpha=0.0)

    fig3 = plt.pcolor(ltd, lat, mydata[:], vmin=119, vmax=240, cmap=my_pallet)
    m = bm.Basemap(projection='cyl', llcrnrlat=8.0, urcrnrlat=16.0, llcrnrlon=-20.0, urcrnrlon=20.0, resolution='f') # fine resolution for grid
    m.drawcoastlines(linewidth=2)
    m.drawcountries(linewidth=1)
    plt.text(-21.5, 15, '(c)')
    plt3_ax = ax1.gca()
    left0, bottom0, width0, height0 = plt3_ax.get_position().bounds
    cbar_3_ax = ax1.add_axes([left0, bottom0 - 0.01, width0, 0.015])
    cb3 = ax1.colorbar(fig3, cax=cbar_3_ax, orientation='horizontal')
    cb3.set_label('Marteau local onset 1998')

    plt.subplots_adjust(hspace=0.3)
    # plt.savefig('matplot_contour_with_basemap.png') # save figure
    plt.show()

if __name__ == "__main__":
    workshop_contour_example_basemap()
