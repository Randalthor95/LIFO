import csv

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go


def print_metrics(network_name, queue_type, packet_generators, packet_sink, switch_ports, port_monitors, time):
    print(network_name.name, queue_type.name)
    for packet_generator in packet_generators:
        print("packet_generator: {}, sent: {}".format(packet_generator.id, packet_generator.packets_sent))
    for switch_port in switch_ports:
        print(" switch_port: {}: received: {}, dropped {}, loss rate: {}".
              format(switch_port.id, switch_port.packets_rec,
                     switch_port.packets_drop, float(switch_port.packets_drop) / switch_port.packets_rec))
    for port_monitor in port_monitors:
        print("average switch occupancy for switch_port", port_monitor.port.id,
              ": {:.3f}".format(float(sum(port_monitor.sizes)) / len(port_monitor.sizes)))
    print("average wait = {:.3f}".format(sum(packet_sink.waits) / len(packet_sink.waits)))
    print("sink {}: bytes per second received: {:.3f} bps,"
          .format(packet_sink.id, float(packet_sink.bytes_rec / time)))
    print("sink {}: average packet size received by sink: {:.3f} bytes"
          .format(packet_sink.id, float(packet_sink.bytes_rec / packet_sink.packets_rec)))
    print()
    # fig, axis = plt.subplots()
    # axis.hist(packet_sink.waits, bins=100, normed=True)
    # axis.set_title("Histogram for waiting times")
    # axis.set_xlabel("time")
    # axis.set_ylabel("normalized frequency of occurrence")
    # fig.savefig("WaitHistogram.png")
    # plt.show()
    # fig, axis = plt.subplots()
    # axis.hist(packet_sink.waits, bins=100, normed=True)
    # axis.set_title("Histogram for System Occupation times")
    # axis.set_xlabel("number")
    # axis.set_ylabel("normalized frequency of occurrence")
    # fig.savefig("QueueHistogram.png")
    # plt.show()
    # fig, axis = plt.subplots()
    # axis.hist(packet_sink.arrivals, bins=10, density=True)
    # axis.set_title("Histogram for Sink Interarrival times")
    # axis.set_xlabel("time")
    # axis.set_ylabel("normalized frequency of occurrence")
    # # fig.savefig("ArrivalHistogram.png")
    # plt.show()


def save_metrics(path, network_name, packet_generator_type, queue_type, packet_generators, packet_sink, switch_ports,
                 port_monitors, time):
    data = []

    # Packet Generators
    pg_ids = ['id']
    packets_sent_data = ['Packets Sent']
    for i in range(len(packet_generators)):
        pg_ids.append(i)
        packets_sent_data.append(packet_generators[i].packets_sent)
    data.append(pg_ids)
    data.append(packets_sent_data)

    # Switches
    switch_ids = ['id']
    packets_received = ['Packets Received']
    packets_dropped = ['Packets Dropped']
    loss_rate = ['Loss Rate']
    buffer_occupancy = ['Average Buffer Occupancy']
    for switch_port in switch_ports:
        switch_ids.append(switch_port.id)
        packets_received.append(switch_port.packets_rec)
        packets_dropped.append(switch_port.packets_drop)
        loss_rate.append(float(switch_port.packets_drop) / switch_port.packets_rec)

    for port_monitor in port_monitors:
        buffer_occupancy.append(float(sum(port_monitor.sizes)) / len(port_monitor.sizes))

    data.append(switch_ids)
    data.append(packets_received)
    data.append(packets_dropped)
    data.append(loss_rate)
    data.append(buffer_occupancy)

    # Sinks
    sink_ids = ['id', packet_sink.id]
    average_wait_time = ['Average Wait Time', (sum(packet_sink.waits) / len(packet_sink.waits))]
    bytes_per_second = ['Bytes per Second', float(packet_sink.bytes_rec / time)]

    data.append(sink_ids)
    data.append(average_wait_time)
    data.append(bytes_per_second)

    print(data)
    with open(network_name + '_' + packet_generator_type.name + '.csv', 'w', newline='', encoding='utf-8') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(data)

    # print_metrics(network_name, queue_type, packet_generators, packet_sink, switch_ports, port_monitors, time)
