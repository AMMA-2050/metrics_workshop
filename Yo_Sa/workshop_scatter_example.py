#######################
#
# workshop_scatter_example.py
#
######################
import matplotlib.pyplot as plt
import numpy

def workshop_scatter_example():
    list1 = numpy.arange(0,1,0.05)
    list2 = numpy.power(list1, 2)
    list3 = numpy.power(list1, 4)
    #list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # some data
    #list2 = [5, 2, 6, 9, 12, 14, 17, 2, 8, 12]  # some other data
    #list3 = [2, 5, 4, 3, 13, 17, 13, 18, 7, 20]
    print(len(list1), len(list2))  # debug test
    #a = 500
    plt.figure(figsize=(6, 6))  # set figure environment
    plt.scatter(list1[:], list2[:],c='r',marker='^',s=50,label='Boys')  # plot basic scatter
    plt.scatter(list1[:], list3[:],label='Girls')
    plt.xlabel('Metric 1')  # label x and y axes
    plt.ylabel('Metric 2 ')
    plt.legend(fontsize=20,loc='best')
    plt.show()  # display

if __name__ == "__main__":       # This statement makes sure that the code is only
    workshop_scatter_example()   # executed if it is run from command line (run as main).
                                 # Not when it is imported by another module
