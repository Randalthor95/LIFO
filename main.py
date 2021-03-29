from random import expovariate
import simpy
import random

from scipy.stats import halfnorm

from SimComponents import PacketGenerator, PacketSink, SwitchPort, QueueType
import matplotlib.pyplot
import numpy as np
import matplotlib.pyplot as plt

def const_arrival():  # Constant arrival distribution for generator 1
    return 1.0


def const_arrival2():
    return 2.0


def dist_size():
    return 2.0


if __name__ == '__main__':
    numargs = halfnorm.numargs
    [] = [0.7, ] * numargs
    rv = halfnorm()

    print("RV : \n", rv)
    quantile = np.arange(0.01, 1, 0.1)

    # Random Variates
    R = halfnorm.rvs(scale=2, size=10)
    print("Random Variates : \n", R)
    distribution = np.linspace(0, np.minimum(rv.dist.b, 3))
    print("Distribution : \n", distribution)

    plot = plt.plot(distribution, rv.pdf(distribution))
    plt.show()
