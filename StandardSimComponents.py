import enum
import functools
import random
import simpy

from DataGeneration import get_metrics
from SimComponents import PacketGenerator, PacketSink, SwitchPort, QueueType, PortMonitor, BurstyPacketGenerator

switch_port_bit_rate = 200000 * 8
switch_port_qlimit = 10000000
time = 200
port_monitor_sampling_distribution = functools.partial(random.expovariate, 1.0)


class PacketGeneratorType(enum.Enum):
    Constant = 1
    Bursty = 2
    Normal = 3
    Exponential = 4


def test_multihop_path(packet_generator_type, queue_type, num_switches):
    env = simpy.Environment()  # Create the SimPy environment

    packet_generator = \
        (packet_generator_type == PacketGeneratorType.Constant
         and standard_constant_packet_generator(env, 'g')) \
        or (packet_generator_type == PacketGeneratorType.Bursty
            and standard_bursty_packet_generator(env, 'g')) \
        or (packet_generator_type == PacketGeneratorType.Normal
            and standard_normal_packet_generator(env, 'g')) \
        or standard_exponential_packet_generator(env, 'g')

    switch_ports = []
    port_monitors = []
    for i in range(num_switches):
        switch_ports.append(SwitchPort(env, id='s' + str(i),
                                   rate=switch_port_bit_rate, qlimit=switch_port_qlimit, queue_type=queue_type))
        port_monitors.append(PortMonitor(env, switch_ports[i], port_monitor_sampling_distribution))

    for i in range(num_switches):
        if i < num_switches - 1:
            switch_ports[i].out = switch_ports[i + 1]

    packet_generator.out = switch_ports[0]
    packet_sink = PacketSink(env, rec_arrivals=True)  # debug: every packet arrival is printed
    switch_ports[num_switches - 1].out = packet_sink
    # Wire packet generators and sinks together
    env.run(until=time)
    get_metrics(packet_generator_type, queue_type, [packet_generator], packet_sink, switch_ports, port_monitors, time)


def test_one_generator_one_switch(packet_generator_type, queue_type):
    env = simpy.Environment()  # Create the SimPy environment
    packet_generator = \
        (packet_generator_type == PacketGeneratorType.Constant and standard_constant_packet_generator(env, 'gA')) \
        or (packet_generator_type == PacketGeneratorType.Bursty and standard_bursty_packet_generator(env, 'gA')) \
        or (packet_generator_type == PacketGeneratorType.Normal and standard_normal_packet_generator(env, 'gA')) \
        or standard_exponential_packet_generator(env, 'gA')

    switch_port = SwitchPort(env, id='s',
                             rate=switch_port_bit_rate, qlimit=switch_port_qlimit, queue_type=queue_type)
    packet_sink = PacketSink(env, rec_arrivals=True)  # debug: every packet arrival is printed
    # Wire packet generators and sinks together
    packet_generator.out = switch_port
    switch_port.out = packet_sink
    port_monitor = PortMonitor(env, switch_port, port_monitor_sampling_distribution)
    env.run(until=time)
    get_metrics(packet_generator_type, queue_type, [packet_generator], packet_sink, [switch_port], [port_monitor], time)


def test_one_of_each_generator_one_switch(queue_type):
    env = simpy.Environment()  # Create the SimPy environment
    constant_packet_generator = standard_constant_packet_generator(env, 'g_constant')
    bursty_packet_generator = standard_bursty_packet_generator(env, 'g_burst')
    normal_packet_generator = standard_normal_packet_generator(env, 'g_normal')
    exponential_packet_generator = standard_exponential_packet_generator(env, 'g_exponential')
    packet_generators = []
    packet_generators.append(constant_packet_generator)
    packet_generators.append(bursty_packet_generator)
    packet_generators.append(normal_packet_generator)
    packet_generators.append(exponential_packet_generator)

    switch_port = SwitchPort(env, id='sA',
                             rate=switch_port_bit_rate, qlimit=switch_port_qlimit, queue_type=queue_type)
    packet_sink = PacketSink(env, rec_arrivals=True)  # debug: every packet arrival is printed
    # Wire packet generators and sinks together
    constant_packet_generator.out = switch_port
    bursty_packet_generator.out = switch_port
    normal_packet_generator.out = switch_port
    exponential_packet_generator.out = switch_port
    switch_port.out = packet_sink
    port_monitor = PortMonitor(env, switch_port, port_monitor_sampling_distribution)
    env.run(until=time)
    get_metrics('One of Each Generator One Switch', queue_type, packet_generators, packet_sink, [switch_port],
                [port_monitor], time)


def test_overloaded_switch(packet_generator_type, queue_type, num_nodes):
    env = simpy.Environment()  # Create the SimPy environment
    switch_port = SwitchPort(env, id='s',
                             rate=switch_port_bit_rate, qlimit=switch_port_qlimit, queue_type=queue_type)
    packet_generators = []
    for i in range(num_nodes):
        packet_generator = \
            (packet_generator_type == PacketGeneratorType.Constant
             and standard_constant_packet_generator(env, 'g' + str(i))) \
            or (packet_generator_type == PacketGeneratorType.Bursty
                and standard_bursty_packet_generator(env, 'g' + str(i))) \
            or (packet_generator_type == PacketGeneratorType.Normal
                and standard_normal_packet_generator(env, 'g' + str(i))) \
            or standard_exponential_packet_generator(env, 'g' + str(i))
        packet_generator.out = switch_port
        packet_generators.append(packet_generator)

    packet_sink = PacketSink(env, rec_arrivals=True)  # debug: every packet arrival is printed
    # Wire packet generators and sinks together
    switch_port.out = packet_sink
    port_monitor = PortMonitor(env, switch_port, port_monitor_sampling_distribution)
    env.run(until=time)
    get_metrics(packet_generator_type, queue_type, packet_generators, packet_sink, [switch_port], [port_monitor], time)


def test_two_good_one_bad(packet_generator_type, queue_type):
    env = simpy.Environment()  # Create the SimPy environment
    packet_generator_good_a = \
        (packet_generator_type == PacketGeneratorType.Constant and standard_constant_packet_generator(env, 'g_good_A')) \
        or (packet_generator_type == PacketGeneratorType.Bursty and standard_bursty_packet_generator(env, 'g_good_A')) \
        or (packet_generator_type == PacketGeneratorType.Normal and standard_normal_packet_generator(env, 'g_good_A')) \
        or standard_exponential_packet_generator(env, 'g_good_A')
    packet_generator_good_b = \
        (packet_generator_type == PacketGeneratorType.Constant and standard_constant_packet_generator(env, 'g_good_B')) \
        or (packet_generator_type == PacketGeneratorType.Bursty and standard_bursty_packet_generator(env, 'g_good_B')) \
        or (packet_generator_type == PacketGeneratorType.Normal and standard_normal_packet_generator(env, 'g_good_B')) \
        or standard_exponential_packet_generator(env, 'g_good_B')
    bad_guy = \
        (packet_generator_type == PacketGeneratorType.Constant and bad_standard_constant_packet_generator(env, 'g_bad')) \
        or (packet_generator_type == PacketGeneratorType.Bursty and bad_standard_bursty_packet_generator(env, 'g_bad')) \
        or (packet_generator_type == PacketGeneratorType.Normal and bad_standard_normal_packet_generator(env, 'g_bad')) \
        or bad_standard_exponential_packet_generator(env, 'g_bad')
    packet_generators = []
    packet_generators.append(packet_generator_good_a)
    packet_generators.append(packet_generator_good_b)
    packet_generators.append(bad_guy)

    switch_port = SwitchPort(env, id='sA',
                             rate=switch_port_bit_rate, qlimit=switch_port_qlimit, queue_type=queue_type)
    packet_sink = PacketSink(env, rec_arrivals=True)  # debug: every packet arrival is printed
    # Wire packet generators and sinks together
    packet_generator_good_a.out = switch_port
    packet_generator_good_b.out = switch_port
    bad_guy.out = switch_port
    switch_port.out = packet_sink
    port_monitor = PortMonitor(env, switch_port, port_monitor_sampling_distribution)
    env.run(until=time)
    get_metrics('One of Each Generator One Switch', queue_type, packet_generators, packet_sink, [switch_port],
                [port_monitor], time)


# Constant  ####################################################################################################

def constant_packet_generator_inter_arrival_rate():  # Constant arrival distribution for generator 1
    return 1 / 300


def constant_packet_size_in_bytes_distribution():
    return 300.0


def standard_constant_packet_generator(env, id):
    return PacketGenerator(env, id, constant_packet_generator_inter_arrival_rate,
                           constant_packet_size_in_bytes_distribution)


def bad_constant_packet_generator_inter_arrival_rate():  # Constant arrival distribution for generator 1
    return 1 / 600


def bad_constant_packet_size_in_bytes_distribution():
    return 600.0


def bad_standard_constant_packet_generator(env, id):
    return PacketGenerator(env, id, bad_constant_packet_generator_inter_arrival_rate,
                           bad_constant_packet_size_in_bytes_distribution)


# Bursty  ####################################################################################################

def norm_packet_generator_inter_arrival_rate():  # Normal arrival distribution for generator 1
    return abs(random.normalvariate(1 / 300, 1 / 100))


def norm_packet_size_in_bytes_distribution():
    return abs(random.normalvariate(800, 300))


def bursty_packet_generator_inter_arrival_rate():
    return abs(random.normalvariate(1 / 11000, 1 / 250))


def bursty_packet_size_in_bytes_distribution():
    return abs(random.normalvariate(9000, 1000))


def burst_rounds_distribution():
    return abs(random.normalvariate(15, 5))


probability_of_burst = .2


def standard_bursty_packet_generator(env, id):
    return BurstyPacketGenerator(env, id, norm_packet_generator_inter_arrival_rate,
                                 norm_packet_size_in_bytes_distribution,
                                 bursty_packet_generator_inter_arrival_rate,
                                 bursty_packet_size_in_bytes_distribution, probability_of_burst,
                                 burst_rounds_distribution)


def bad_norm_packet_generator_inter_arrival_rate():  # Normal arrival distribution for generator 1
    return abs(random.normalvariate(1 / 600, 1 / 100))


def bad_norm_packet_size_in_bytes_distribution():
    return abs(random.normalvariate(1600, 300))


def bad_bursty_packet_generator_inter_arrival_rate():
    return abs(random.normalvariate(1 / 22000, 1 / 250))


def bad_bursty_packet_size_in_bytes_distribution():
    return abs(random.normalvariate(18000, 1000))


def bad_burst_rounds_distribution():
    return abs(random.normalvariate(15, 5))


bad_probability_of_burst = .2


def bad_standard_bursty_packet_generator(env, id):
    return BurstyPacketGenerator(env, id, bad_norm_packet_generator_inter_arrival_rate,
                                 bad_norm_packet_size_in_bytes_distribution,
                                 bad_bursty_packet_generator_inter_arrival_rate,
                                 bad_bursty_packet_size_in_bytes_distribution, bad_probability_of_burst,
                                 bad_burst_rounds_distribution)


# Normal  ####################################################################################################

def normal_packet_generator_inter_arrival_rate():  # Constant arrival distribution for generator 1
    return abs(random.normalvariate(1 / 1000, 1 / 250))


def normal_packet_size_in_bytes_distribution():
    return abs(random.normalvariate(800, 300))


def standard_normal_packet_generator(env, id):
    return PacketGenerator(env, id, normal_packet_generator_inter_arrival_rate,
                           normal_packet_size_in_bytes_distribution)


def bad_normal_packet_generator_inter_arrival_rate():  # Constant arrival distribution for generator 1
    return abs(random.normalvariate(1 / 2000, 1 / 250))


def bad_normal_packet_size_in_bytes_distribution():
    return abs(random.normalvariate(1600, 300))


def bad_standard_normal_packet_generator(env, id):
    return PacketGenerator(env, id, bad_normal_packet_generator_inter_arrival_rate,
                           bad_normal_packet_size_in_bytes_distribution)


# Exponential  ####################################################################################################

def exponential_packet_generator_inter_arrival_rate():  # Constant arrival distribution for generator 1
    return abs(random.expovariate(300))


def exponential_packet_size_in_bytes_distribution():
    return abs(random.expovariate(1 / 300))


def standard_exponential_packet_generator(env, id):
    return PacketGenerator(env, id, exponential_packet_generator_inter_arrival_rate,
                           exponential_packet_size_in_bytes_distribution)


def bad_exponential_packet_generator_inter_arrival_rate():  # Constant arrival distribution for generator 1
    return abs(random.expovariate(600))


def bad_exponential_packet_size_in_bytes_distribution():
    return abs(random.expovariate(1 / 600))


def bad_standard_exponential_packet_generator(env, id):
    return PacketGenerator(env, id, bad_exponential_packet_generator_inter_arrival_rate,
                           bad_exponential_packet_size_in_bytes_distribution)
