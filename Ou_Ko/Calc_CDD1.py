#########################################
#
# Calc_CDD
#
#########################################
def TRMM_CDD(yyyy,total):
   import numpy as np
   import matplotlib.pyplot as plt
   from numpy import genfromtxt as gent
   from netCDF4 import Dataset
   import mpl_toolkits.basemap as bm    
   
 # first bring in the data
   
   dtes = []
   duration = []
   pltdtes = np.zeros((my_trmm.shape[1],my_trmm.shape[2]),dtype = int)
   pltdur = np.zeros((my_trmm.shape[1],my_trmm.shape[2]),dtype = int)
   for x in range(0,my_trmm.shape[2]):
       for y in range(0,my_trmm.shape[1]):
           current_max = 0
           current_dte = 0
           dte = 0
           duratn = 0
           if my_data[y,x]-119 > my_trmm.shape[0]-10 or my_data[y,x] >= 250:
               continue
           else:    
              for t in range(int(my_data[y,x])-119, my_trmm.shape[0]-10):
                  if my_trmm[t,y,x] <= float(total):
                      dte = t
                      print dte
                      for t1 in xrange(t,my_trmm.shape[0] - 10):
                          if my_trmm[t1,y,x] <= float(total):
                              continue
                          else:
                              duratn = t1 - t
                              if duratn > current_max:
                                  current_dte = dte + 119
                                  current_max = duratn
                          break
           dtes.extend([current_dte])
           duration.extend([current_max])
           pltdtes[y,x] = current_dte
           pltdur[y,x] = current_max
                  
  #                else:
  #                  continue
  #                break                            
   print np.max(duration[:])
   print np.max(dtes[:])                  
#   plt.clf()
#   plt.scatter(duration[:],dtes[:])
#   plt.show() 
   plt.clf()
   levs1 = [119,129,139,150,160,170,180,190,200,211,221,231,242]
   dates = ['1/5','11/5','21/5','1/6','11/6','21/6','1/7','11/7','21/7','1/8','11/8','21/8','1/9']
   levs2 = [2,4,6,8,10,12,15,18,20]
   ltd = np.linspace(-17.5,-11.5,24)
   lati = np.linspace(11,16,20)   
   ax1 = plt.figure(figsize = (12,12))
   plt.subplot(2,1,1)
   m = bm.Basemap(projection='cyl',llcrnrlat = 11, urcrnrlat = 16, llcrnrlon = -17.5, urcrnrlon = -11.5,  resolution = 'c')   
   fig2 = plt.contourf(ltd,lati,pltdtes[:],levs1,extend='max')
   m.drawcoastlines(linewidth= 2)
   m.drawcountries(linewidth = 1)
   plt2_ax = ax1.gca()     
   left0, bottom0, width0, height0 = plt2_ax.get_position().bounds   
   cbar_1_ax = ax1.add_axes([left0, bottom0 - 0.05, width0, 0.015])
   cb2 = ax1.colorbar(fig2, cax = cbar_1_ax, orientation = 'horizontal')
   cb2.set_label('Date of longest dry spell (after onset)')
   cb2.set_ticks(levs1)
   cb2.set_ticklabels(dates)
   plt.subplot(2,1,2)
   m = bm.Basemap(projection='cyl',llcrnrlat = 11, urcrnrlat = 16, llcrnrlon = -17.5, urcrnrlon = -11.5,  resolution = 'c')      
   fig2 = plt.contourf(ltd,lati,pltdur[:],levs2,extend='max')
   m.drawcoastlines(linewidth= 2)
   m.drawcountries(linewidth = 1)
   plt2_ax = ax1.gca()     
   left0, bottom0, width0, height0 = plt2_ax.get_position().bounds   
   cbar_1_ax = ax1.add_axes([left0, bottom0 - 0.05, width0, 0.015])
   cb2 = ax1.colorbar(fig2, cax = cbar_1_ax, orientation = 'horizontal')
   cb2.set_label('Duration of first dry spell')
   plt.subplots_adjust(hspace = 0.5)
  # plt.savefig('TRMM_CDD_'+str(yyyy)+'_limit'+str(total)+'mm_per_day.png')
   plt.show()
   np.savetxt('CDD_date_'+str(yyyy)+'.csv', pltdtes[:], delimiter = ',') 
   np.savetxt('CDD_duration_'+str(yyyy)+'.csv', pltdur[:], delimiter = ',')       
    
if "__name__" == "__TRMM_CDD__":
    TRMM_CDD(yyyy)    