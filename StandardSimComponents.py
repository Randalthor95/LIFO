import enum
import functools
import random
import simpy

from DataGeneration import get_metrics
from SimComponents import PacketGenerator, PacketSink, SwitchPort, QueueType, PortMonitor, BurstyPacketGenerator

switch_port_bit_rate = 200000 * 8
switch_port_qlimit = 2500
time = 200
port_monitor_sampling_distribution = functools.partial(random.expovariate, 1.0)


class PacketGeneratorType(enum.Enum):
    Constant = 1
    Bursty = 2
    Normal = 3
    Exponential = 4


def test_one_generator_one_switch(packet_generator_type, queue_type):
    env = simpy.Environment()  # Create the SimPy environment
    packet_generator = \
        (packet_generator_type == PacketGeneratorType.Constant and standard_constant_packet_generator(env, 'gA')) \
        or (packet_generator_type == PacketGeneratorType.Bursty and standard_burst_packet_generator(env, 'gA')) \
        or (packet_generator_type == PacketGeneratorType.Normal and standard_normal_packet_generator(env, 'gA')) \
        or standard_exponential_packet_generator(env, 'gA')

    switch_port = SwitchPort(env, id='sA',
                             rate=switch_port_bit_rate, qlimit=switch_port_qlimit, queue_type=queue_type)
    packet_sink = PacketSink(env, rec_arrivals=True)  # debug: every packet arrival is printed
    # Wire packet generators and sinks together
    packet_generator.out = switch_port
    switch_port.out = packet_sink
    port_monitor = PortMonitor(env, switch_port, port_monitor_sampling_distribution)
    env.run(until=time)
    get_metrics(packet_generator_type, queue_type, packet_generator, packet_sink, switch_port, port_monitor, time)


# Constant  ####################################################################################################

def constant_packet_generator_inter_arrival_rate():  # Constant arrival distribution for generator 1
    return 1 / 500


def constant_packet_size_in_bytes_distribution():
    return 500.0


def standard_constant_packet_generator(env, id):
    return PacketGenerator(env, id, constant_packet_generator_inter_arrival_rate,
                           constant_packet_size_in_bytes_distribution)


# Bursty  ####################################################################################################

def norm_packet_generator_inter_arrival_rate():  # Normal arrival distribution for generator 1
    return abs(random.normalvariate(1 / 10, 1 / 200))


def norm_packet_size_in_bytes_distribution():
    return abs(random.normalvariate(10.0, 10.0))


def bursty_packet_generator_inter_arrival_rate():  # Constant arrival distribution for generator 1
    return abs(random.normalvariate(1 / 1000, 1 / 200))


def bursty_packet_size_in_bytes_distribution():
    return abs(random.normalvariate(1000.0, 500))


def burst_rounds_distribution():
    return abs(random.normalvariate(5, 10))


probability_of_burst = .3


def standard_burst_packet_generator(env, id):
    return BurstyPacketGenerator(env, id, norm_packet_generator_inter_arrival_rate,
                                 norm_packet_size_in_bytes_distribution,
                                 bursty_packet_generator_inter_arrival_rate,
                                 bursty_packet_size_in_bytes_distribution, probability_of_burst,
                                 burst_rounds_distribution)


# Normal  ####################################################################################################

def normal_packet_generator_inter_arrival_rate():  # Constant arrival distribution for generator 1
    return abs(random.normalvariate(1 / 1000, 1 / 200))


def normal_packet_size_in_bytes_distribution():
    return abs(random.normalvariate(600, 300))


def standard_normal_packet_generator(env, id):
    return PacketGenerator(env, id, normal_packet_generator_inter_arrival_rate,
                           normal_packet_size_in_bytes_distribution)


# Exponential  ####################################################################################################

def exponential_packet_generator_inter_arrival_rate():  # Constant arrival distribution for generator 1
    return abs(random.expovariate(1000))


def exponential_packet_size_in_bytes_distribution():
    return abs(random.expovariate(1/500))


def standard_exponential_packet_generator(env, id):
    return PacketGenerator(env, id, exponential_packet_generator_inter_arrival_rate,
                           exponential_packet_size_in_bytes_distribution)

