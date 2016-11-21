#######################
#
# workshop_scatter_example.py
#
######################

def workshop_scatter_example_with_modifications(a):
   import matplotlib.pyplot as plt
   
   list1 = [1,2,3,4,5,6,7,8,9,10] # some data
   list2 = [5,2,6,9,12,14,17,2,8,12] #some other data
   list3 = [10,9,8,7,6,5,4,3,2,1] 
   print len(list1), len(list2) # debug test
   
   plt.clf() # clear the plt environment
   plt.figure(figsize = (6,6)) # set figure environment
   plt.scatter(list1[:],list2[:],c='r',marker = '^', s = 100, label = "list1 v list2") # plot basic scatter
   plt.scatter(list1[:],list3[:],c = 'k',marker = '*', s = 150, label = "list1 v list3")
   plt.xlabel('Metric 1') #label x and y axes
   plt.ylabel('Metric 2')
   plt.legend(fontsize = 10, loc = 'best')
   plt.show()  #d isplay
    
    
if "__name__" == "__workshop_scatter_example_with_modifications__":
 workshop_scatter_example_with_modifications(a)    