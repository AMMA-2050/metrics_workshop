#######################
#
# workshop_scatter_example.py
#
######################

import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt as gent

def workshop_contour_example_basic():

   # this is only working when the .csv file is in the same folder as your script
   #If your script can't find the file, check your path!
   mydata = gent('/nfs/see-fs-01_teaching/earv056/metrics_workshop/example_code/TRMM_v7_Marteau_onsets_1998_dry_spell_30.csv', delimiter = ',')

   print(mydata.shape[:])
   ltd = np.linspace(-20,20,160)
   lat = np.linspace(8.0,16.0,32)

   fig1 = plt.figure(figsize = (10,7)) # open figure window

   plt.subplot(3,1,1)                  # subplot 1
   ax1 = plt.contour(ltd,lat,mydata[:])

   plt.subplot(3,1,2)                  # subplot 2
   ax2 = plt.contourf(ltd,lat,mydata[:])

   plt.subplot(3,1,3)                  # subplot 3
   ax3 = plt.pcolor(ltd,lat,mydata[:], vmin = 119, vmax = 240)
   plt.savefig('onset1.png')
   plt.show()
   
    
if __name__ == "__main__":
   workshop_contour_example_basic()