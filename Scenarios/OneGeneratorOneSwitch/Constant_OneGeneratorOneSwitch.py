import functools
import random
import simpy

from DataGeneration import get_metrics
from SimComponents import PacketGenerator, PacketSink, SwitchPort, QueueType, PortMonitor


def const_arrival():  # Constant arrival distribution for generator 1
    return 1.0


def const_arrival2():
    return 2.0


def dist_size():
    return 2.0

samp_dist = functools.partial(random.expovariate, 1.0)
time = 2000

if __name__ == '__main__':
    env = simpy.Environment()  # Create the SimPy environment
    packet_generator = PacketGenerator(env, "gA", const_arrival, dist_size, finish=5.0)
    switch_port = SwitchPort(env, id='sA', rate=2.0, qlimit=300, queue_type=QueueType.RANDO)
    packet_sink = PacketSink(env, rec_arrivals=True)  # debug: every packet arrival is printed
    # Wire packet generators and sinks together
    packet_generator.out = switch_port
    switch_port.out = packet_sink
    port_monitor = PortMonitor(env, switch_port, samp_dist)
    env.run(until=time)
    packet_sink.arrivals
    get_metrics(packet_generator, packet_sink, switch_port, port_monitor, time)
