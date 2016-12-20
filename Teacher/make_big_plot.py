'''
'''

import matplotlib.pyplot as plt
import iris

def make_big_plot(incube):
    plt.clf()
    cntr = 1
    for t in incube.coord('model_name'):
        cube2plot = iris.extract(incube,model_name = t)
        plt.subplot(6,5,cntr)
        plt.contourf(cube2plot)
        cntr = cntr + 1
    plt.show()



if __name__ == "__main__":
    make_big_plot(incube)