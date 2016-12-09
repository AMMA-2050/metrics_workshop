#######################
#
# workshop_scatter_example.py
#
######################

def workshop_hist_example_full(a,b):
   import matplotlib.pyplot as plt
   import scipy.stats as stat

   list1 = [1,2,3,4,5,6,7,8,9,10] # some data
   
   plt.clf() # clear the plt environment
   plt.figure(figsize = (6,6)) # set figure environment
   plt.hist(b[:],a[:]) # plot basic scatter
#   plt.scatter(list1[:],list3[:],c = 'k',marker = '*', s = 150, label = 'correl = '+str(correl2))
   plt.xlabel('Metric 1') #label x and y axes
   plt.ylabel('Metric 2')
#   plt.legend(fontsize = 10, loc = 'best')
#   plt.set_ylim(0,15)
#   plt.set_xlim(0,10)
   plt.text(-2,13,'(a)')
   plt.title('Subplot Title')
   plt.suptitle('Whole Plot Title')
   
   plt.show()  #d isplay
    
    
if "__name__" == "__workshop_hist_example_full__":
 workshop_hist_example_full(a)    