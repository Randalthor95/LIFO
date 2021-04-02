import matplotlib.pyplot as plt


def get_metrics(network_name, queue_type, packet_generators, packet_sink, switch_ports, port_monitors, time):
    print(network_name, queue_type.name)
    print("average wait = {:.3f}".format(sum(packet_sink.waits) / len(packet_sink.waits)))
    for switch_port in switch_ports:
        print(" port: {}: received: {}, dropped {}, loss rate: {}".
              format(switch_port.id, switch_port.packets_rec, switch_port.packets_drop, float(
                switch_port.packets_drop) / switch_port.packets_rec))
    for packet_generator in packet_generators:
        print("id: {}, sent: {}".format(packet_generator.id, packet_generator.packets_sent))
    for port_monitor in port_monitors:
        print("average switch occupancy for", port_monitor.port.id,
              ": {:.3f}".format(float(sum(port_monitor.sizes)) / len(port_monitor.sizes)))
    print("bytes per second: {:.3f}".format(float(packet_sink.bytes_rec / time)))
    print("average packet size: {:.3f} bytes".format(float(packet_sink.bytes_rec / packet_sink.packets_rec)))
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
    fig, axis = plt.subplots()
    axis.hist(packet_sink.arrivals, bins=10, density=True)
    axis.set_title("Histogram for Sink Interarrival times")
    axis.set_xlabel("time")
    axis.set_ylabel("normalized frequency of occurrence")
    # fig.savefig("ArrivalHistogram.png")
    plt.show()
