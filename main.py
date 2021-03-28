from random import expovariate
import simpy
import random
from SimComponents import PacketGenerator, PacketSink, SwitchPort, QueueType


def const_arrival():  # Constant arrival distribution for generator 1
    return 1.0


def const_arrival2():
    return 2.0


def dist_size():
    return 2.0


if __name__ == '__main__':
    print("Here is a single sample from a uniform random variable")
    print(random.random())
    print("Here is a list of three samples:")
    uniSamples = [random.random(), random.random(), random.random()]
    print(uniSamples)
    print("Here is a list of 10 exponential samples:")
    expSamples = []
    for x in range(10):
        expSamples.append(random.uniform(0.01, 1))
    print(expSamples)
