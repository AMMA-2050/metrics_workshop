#######################
#
# workshop_scatter_example.py
#
######################

import matplotlib.pyplot as plt
import numpy as np  # handles arrays

def workshop_scatter_example():
    list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # some data
    list2 = [5, 2, 6, 9, 12, 14, 17, 2, 8, 12]  # some other data
    list3=np.arange(4,14)
    print(len(list1), len(list2),len(list3) )  # debug test
    a=500
    plt.figure(figsize=(6, 6))  # set figure environment
    plt.scatter(list1[:], list2[:],c='b',marker='*',s=300,label='Boys')  # plot basic scatter
    plt.scatter(list1[:], list3[:],c='r',marker='*',s=100,label='Girls')  # plot basic scatter
    plt.grid()
    #plt.rc('grid', linestyle="*", color='blue')
    #plt.xlabel('Metric 1')  # label x and y axes
    #plt.ylabel('Metric 2')
    plt.xlabel('Age')  # label x and y axes ad siny
    plt.ylabel('Do they like cakes? +str(a)')   
    
    plt.legend(fontsize=12,loc='best')
    
    plt.show()  # display
    #plt.legend(fontsize=num,loc='best')

if __name__ == "__main__":       # This statement makes sure that the code is only
    workshop_scatter_example()   # executed if it is run from command line (run as main).
                                 # Not when it is imported by another module
