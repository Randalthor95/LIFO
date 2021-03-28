import functools
import random
import simpy
import math

from DataGeneration import get_metrics
from SimComponents import PacketGenerator, PacketSink, SwitchPort, QueueType, PortMonitor


def packet_generator_inter_arrival_rate():  # Constant arrival distribution for generator 1
    return 1/1000


def packet_size_in_bytes_distribution():
    return 1000.0


switch_port_bit_rate = 2000000 * 8
switch_port_qlimit = 2500
time = 2000
port_monitor_sampling_distribution = functools.partial(random.expovariate, 1.0)


if __name__ == '__main__':
    env = simpy.Environment()  # Create the SimPy environment
    packet_generator = PacketGenerator(env, "gA", packet_generator_inter_arrival_rate,
                                       packet_size_in_bytes_distribution)
    switch_port = SwitchPort(env, id='sA',
                             rate=switch_port_bit_rate, qlimit=switch_port_qlimit, queue_type=QueueType.FIFO)
    packet_sink = PacketSink(env, rec_arrivals=True)  # debug: every packet arrival is printed
    # Wire packet generators and sinks together
    packet_generator.out = switch_port
    switch_port.out = packet_sink
    port_monitor = PortMonitor(env, switch_port, port_monitor_sampling_distribution)
    env.run(until=time)
    get_metrics(packet_generator, packet_sink, switch_port, port_monitor, time)