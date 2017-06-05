'''
'''

import matplotlib.pyplot as plt
import iris

def make_big_plot(incube):
    plt.clf()
    cntr = 1
    modelnums = incube.coord('model_name').points
    for t in modelnums:
	print t
        slicer = iris.Constraint(model_name = str(t))
        cube2plot = incube.extract(slicer)
#        print cube2plot
        plt.subplot(6,5,cntr)
        plt.contourf(cube2plot[:,:].data)
        cntr = cntr + 1
    plt.show()



if __name__ == "__main__":
    make_big_plot(incube)
