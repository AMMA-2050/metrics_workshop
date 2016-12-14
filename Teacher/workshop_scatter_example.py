#######################
#
# workshop_scatter_example.py
#
######################

import matplotlib.pyplot as plt

def workshop_scatter_example():
    list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # some data
    list2 = [5, 2, 6, 9, 12, 14, 17, 2, 8, 12]  # some other data
    list3 = [2,3,4,5,6,1,2,7,8,9]
    print(len(list1), len(list2))  # debug test
    a =500
    plt.figure()  # set figure environment
    plt.scatter(list1[:], list2[:],c='burlywood',marker='*',s=300,label='Boys')  # plot basic scatter
    plt.scatter(list1[:],list3[:],c='r',marker='^',s=100,label = 'Girls')
    plt.xlabel('Age')  # label x and y axes
    plt.ylabel('Do they like cake? ')
    plt.show()  # display

if __name__ == "__main__":       # This statement makes sure that the code is only
    workshop_scatter_example()   # executed if it is run from command line (run as main).
                                 # Not when it is imported by another module
