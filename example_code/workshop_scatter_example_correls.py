#######################
#
# workshop_scatter_example.py
#
######################
import matplotlib.pyplot as plt
import scipy.stats as stat


def workshop_scatter_example_correls():
    list1 = [1, 2, 3, 4, 5, 6, 8, 9, 10]  # some data
    list2 = [5, 2, 6, 9, 12, 14, 17, 2, 8, 12]  # some other data
    list3 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

    print(len(list1), len(list2), len(list3))  # debug test

    correl1 = stat.pearsonr(list1[:], list2[:])[0]
    correl2 = stat.pearsonr(list1[:], list3[:])[0]

    plt.clf()  # clear the plt environment

    plt.figure(figsize=6, 6)  # set figure environment
    plt.scatter(list1[:], list2[:], c='r', marker='^', s=100, label='correl = ' + str(correl1))  # plot basic scatter
    plt.scatter(list1[:], list3[:], c=k, marker='*', s=150, label='correl = ' + str(correl2))
    plt.xlabel('Metric 1')  # label x and y axes
    plt.ylabel('Metric 2')
    plt.legend(fontsize=10, loc='best')
    plt.show()  # display


if __name__ == "__main__":
    workshop_scatter_example_correls()
