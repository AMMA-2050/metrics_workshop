#######################
#
# workshop_scatter_example.py
#
######################

def workshop_scatter_example_full(a):
   import matplotlib.pyplot as plt
   import scipy.stats as stat
# Note here, it is also possible to feed in data either via a subroutine or via other 
# code. Please use the below examples if you want to do one of these.
#####################################################################################
#
# have lists fed in by another code:
#
# e.g. if in line 7, "a" is now a list
# change list1 for "a" 
##################################################################################
#
# pull list from a csv file
#
# lines to add:
# from numpy import genfromtxt as gent
# mydata = gent('file',delimiter = ',')
# list1 = mydata[bounds]
#
###################################################################################  
   list1 = [1,2,3,4,5,6,7,8,9,10] # some data
   list2 = [5,2,6,9,12,14,17,2,8,12] #some other data
   list3 = [10,9,8,7,6,5,4,3,2,1]
   print len(list1), len(list2) # debug test
   correl1 = stat.pearsonr(list1[:],list2[:])[0]
   correl2 = stat.pearsonr(list1[:],list3[:])[0] 
   
   plt.clf() # clear the plt environment
   plt.figure(figsize = (6,6)) # set figure environment
   plt.scatter(list1[:],list2[:],c='r',marker = '^', s = 100, label = 'correl = '+str(correl1)) # plot basic scatter
   plt.scatter(list1[:],list3[:],c = 'k',marker = '*', s = 150, label = 'correl = '+str(correl2))
   plt.set_xlabel('Metric 1') #label x and y axes
   plt.set_ylabel('Metric 2')
   plt.legend(fontsize = 10, loc = 'best')
   plt.set_ylim(0,15)
   plt.set_xlim(0,10)
   plt.text(-2,13,'(a)')
   plt.title('Subplot Title')
   plt.suptitle('Whole Plot Title')
   
   plt.show()  #d isplay
    
    
if "__name__" == "__workshop_scatter_example_full__":
 workshop_scatter_example_full(a)    