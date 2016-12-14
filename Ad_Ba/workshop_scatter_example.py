#######################
#
# workshop_scatter_example.py
#
######################

import matplotlib.pyplot as plt
from numpy.random import random
from mpl_toolkits.mplot3d import Axes3D

def workshop_scatter_example():
    list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # some data
    list2 = [5, 2, 6, 9, 12, 14, 17, 2, 8, 12]  # some other data
    list3 = [15, 6, 17, 11, 19, 7, 9, 12, 13, 14]
    print(len(list1), len(list2))  # debug test
    
    plt.figure()  # set figure environment
    plt.subplot(111, projection='3d')
    plt.scatter(list1[:], list2[:], c='r', marker='*', s= 120, label='boys')  # plot basic scatter
    plt.scatter(list1[:], list3[:], c='g', marker='^', s= 100, label='girls')  # plot basic scatter
    plt.xlabel('Metric 1')  # label x and y axes
    plt.ylabel('Metric 2')
    plt.legend(fontsize=20, loc= 'best')
    plt.show()  # display

if __name__ == "__main__":       # This statement makes sure that the code is only
    workshop_scatter_example()   # executed if it is run from command line (run as main).
                                 # Not when it is imported by another module
