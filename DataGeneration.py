import random
import functools
import simpy
import matplotlib.pyplot as plt
from SimComponents import PacketGenerator, PacketSink, SwitchPort, PortMonitor


def get_metrics(packet_generator, packet_sink, switch_port, port_monitor, time):
    print("average wait = {:.3f}".format(sum(packet_sink.waits) / len(packet_sink.waits)))
    print(
        "received: {}, dropped {}, sent {}".format(switch_port.packets_rec, switch_port.packets_drop,
                                                   packet_generator.packets_sent))
    print("loss rate: {}".format(float(switch_port.packets_drop) / switch_port.packets_rec))
    print("average switch occupancy for", port_monitor.port.id,
          ": {:.3f}".format(float(sum(port_monitor.sizes)) / len(port_monitor.sizes)))
    print("bytes per second: {:.3f}".format(float(packet_sink.bytes_rec / time)))
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
    fig, axis = plt.subplots()
    axis.hist(packet_sink.arrivals, bins=10, density=True)
    axis.set_title("Histogram for Sink Interarrival times")
    axis.set_xlabel("time")
    axis.set_ylabel("normalized frequency of occurrence")
    # fig.savefig("ArrivalHistogram.png")
    plt.show()
