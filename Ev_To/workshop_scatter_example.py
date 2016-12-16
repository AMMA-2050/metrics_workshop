#######################
#
# workshop_scatter_example.py
#
######################

import matplotlib.pyplot as plt

def workshop_scatter_example():
    list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # some data
    list2 = [5, 2, 6, 9, 12, 14, 17, 2, 8, 12]  # some other data
    list3 = [13, 2, 16, 30, 12, 8, 20, 25, 8, 1] #my new data
    list4 = [1, 4, 6, 3, 23, 40, 7, 11, 7.2, 3]
    print(len(list1), len(list2))  # debug test

    plt.figure(figsize=(6, 6))  # set figure environment
    plt.scatter(list1[:], list2[:],c ='y',marker='H', s=100, label='name')  # plot basic scatter
    plt.scatter(list1[:], list3[:],c ='pink',marker='<', s=200, label='day') #line I add
    plt.scatter(list1[:], list3[:],c ='purple',marker='D', s=300, label='month')
    plt.legend(fontsize=12, loc = 'best')
   # plt.xlabel('Metric 1')  # label x and y axes
    #plt.ylabel('Metric 2')
    plt.show()  # display

if __name__ == "__main__":       # This statement makes sure that the code is only
    workshop_scatter_example()   # executed if it is run from command line (run as main).
                                 # Not when it is imported by another module
