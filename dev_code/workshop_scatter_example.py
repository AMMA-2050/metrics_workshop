#######################
#
# workshop_scatter_example.py
#
######################

def workshop_scatter_example(a):
   import matplotlib.pyplot as plt
   
   list1 = [1,2,3,4,5,6,7,8,9,10] # some data
   list2 = [5,2,6,9,12,14,17,2,8,12] #some other data 
   print len(list1), len(list2) # debug test
   
   plt.clf() # clear the plt environment
   plt.figure(figsize = (6,6)) # set figure environment
   plt.scatter(list1[:],list2[:]) # plot basic scatter
   plt.xlabel('Metric 1') #label x and y axes
   plt.ylabel('Metric 2')
   plt.show()  #d isplay
    
    
if "__name__" == "__workshop_scatter_example__":
 workshop_scatter_example(a)    