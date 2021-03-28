"""
Simple example of PacketGenerator, SwitchPort, and PacketSink from the SimComponents module.
Creates constant rate packet generator, connects it to a slow switch port, and then
connects the switch port to a sink. The queue size is made small an the port speed slow
to verify packet drops.

Copyright 2014 Dr. Greg M. Bernstein
Released under the MIT license
"""
from random import expovariate

import simpy
from SimComponents import PacketGenerator, PacketSink, SwitchPort, QueueType


def constArrival():  # Constant arrival distribution for generator 1
    return 1.0

def constArrival2():
    return 2.0

def distSize():
    return 2.0

if __name__ == '__main__':
    env = simpy.Environment()  # Create the SimPy environment
    pg = PacketGenerator(env, "SJSU", constArrival, distSize, finish=5.0)
    switch_port = SwitchPort(env, rate=2.0, qlimit=300, queue_type=QueueType.RANDO, debug=True)
    ps = PacketSink(env, debug=True)  # debug: every packet arrival is printed
    # Wire packet generators and sinks together
    pg.out = switch_port
    switch_port.out = ps
    env.run(until=200)
    print("waits: {}".format(ps.waits))
    print("received: {}, dropped {}, sent {}".format(ps.packets_rec,
         switch_port.packets_drop, pg.packets_sent))