#######################
#
# workshop_scatter_example.py
#
######################

def workshop_contour_example_basic(a):
   import matplotlib.pyplot as plt
   import scipy.stats as stat
   import numpy as np
   from numpy import genfromtxt as gent
   mydata = gent('C:\Users\js08rgjf\Canopy\scripts\csvs\paper_1_codes\TRMM_v7_Marteau_onsets_1998_dry_spell_30.csv',delimiter = ',')
   print mydata.shape[:]  
   ltd = np.linspace(-20,20,160)
   lat = np.linspace(8.0,16.0,32)
   
   plt.clf()
   fig1 = plt.figure(figsize = (10,7))
   plt.subplot(3,1,1)
   ax1 = plt.contour(ltd,lat,mydata[:])
   plt.subplot(3,1,2)
   ax2 = plt.contourf(ltd,lat,mydata[:])
   plt.subplot(3,1,3)
   ax3 = plt.pcolor(ltd,lat,mydata[:], vmin = 119, vmax = 240)
   plt.show()
   
    
if "__name__" == "__workshop_contour_example_basic__":
 workshop_contour_example_basic(a)    