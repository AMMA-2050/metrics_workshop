#######################
#
# workshop_scatter_example.py
#
######################

import matplotlib.pyplot as plt

def workshop_scatter_example():
    list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # some data
    list2 = [5, 2, 6, 9, 12, 14, 17, 2, 8, 12]  # some other data
    list3= [10, 2, 8, 6, 1, 9, 4, 3, 7, 12]
    print(len(list1), len(list2), len(list3))  # debug test
    a=500
    plt.figure(figsize=(6, 6))  # set figure environment
    plt.scatter(list1[:], list2[:],c='r',marker='^', s=50, label='boys')  # plot basic scatter
    plt.scatter(list1[:], list3[:],c='b',marker='*', s=60, label='Girls') 
    plt.xlabel('age')  # label x and y axes
    plt.ylabel('Do they like cake?'+str(a))
    plt.legend(fontsize=10, loc='best')
    plt.show()  # display

if __name__ == "__main__":       # This statement makes sure that the code is only
    workshop_scatter_example()   # executed if it is run from command line (run as main).
                                 # Not when it is imported by another module
