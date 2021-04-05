import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go


def get_metrics(network_name, queue_type, packet_generators, packet_sink, switch_ports, port_monitors, time):
    print(network_name.name, queue_type.name)
    print("average wait = {:.3f}".format(sum(packet_sink.waits) / len(packet_sink.waits)))
    for packet_generator in packet_generators:
        print("packet_generator: {}, sent: {}".format(packet_generator.id, packet_generator.packets_sent))
    for switch_port in switch_ports:
        print(" switch_port: {}: received: {}, dropped {}, loss rate: {}".
              format(switch_port.id, switch_port.packets_rec,
                     switch_port.packets_drop, float(switch_port.packets_drop) / switch_port.packets_rec))
    for port_monitor in port_monitors:
        print("average switch occupancy for switch_port", port_monitor.port.id,
              ": {:.3f}".format(float(sum(port_monitor.sizes)) / len(port_monitor.sizes)))
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


def save_metrics(path, network_name, queue_type, packet_generators, packet_sink, switch_ports, port_monitors, time):
    data = []
    data.append(network_name.name)
    data.append(queue_type.name)
    generators = []
    generators.append('packet_generators')
    print_table(path, data)
    return
    print("average wait = {:.3f}".format(sum(packet_sink.waits) / len(packet_sink.waits)))
    for packet_generator in packet_generators:
        print("packet_generator: {}, sent: {}".format(packet_generator.id, packet_generator.packets_sent))
    for switch_port in switch_ports:
        print(" switch_port: {}: received: {}, dropped {}, loss rate: {}".
              format(switch_port.id, switch_port.packets_rec,
                     switch_port.packets_drop, float(switch_port.packets_drop) / switch_port.packets_rec))
    for port_monitor in port_monitors:
        print("average switch occupancy for switch_port", port_monitor.port.id,
              ": {:.3f}".format(float(sum(port_monitor.sizes)) / len(port_monitor.sizes)))
    print("sink {}: bytes per second received: {:.3f} bps,"
          .format(packet_sink.id, float(packet_sink.bytes_rec / time)))
    print("sink {}: average packet size received by sink: {:.3f} bytes"
          .format(packet_sink.id, float(packet_sink.bytes_rec / packet_sink.packets_rec)))

def print_table(path, data):
    import plotly.graph_objects as go

    values = [['Salaries', 'Office', 'Merchandise', 'Legal', '<b>TOTAL<br>EXPENSES</b>'],  # 1st col
              [
                  "Lorem ipsum dolor sit amet, tollit discere inermis pri ut. Eos ea iusto timeam, an prima laboramus vim. Id usu aeterno adversarium, summo mollis timeam vel ad",
                  "Lorem ipsum dolor sit amet, tollit discere inermis pri ut. Eos ea iusto timeam, an prima laboramus vim. Id usu aeterno adversarium, summo mollis timeam vel ad",
                  "Lorem ipsum dolor sit amet, tollit discere inermis pri ut. Eos ea iusto timeam, an prima laboramus vim. Id usu aeterno adversarium, summo mollis timeam vel ad",
                  "Lorem ipsum dolor sit amet, tollit discere inermis pri ut. Eos ea iusto timeam, an prima laboramus vim. Id usu aeterno adversarium, summo mollis timeam vel ad",
                  "Lorem ipsum dolor sit amet, tollit discere inermis pri ut. Eos ea iusto timeam, an prima laboramus vim. Id usu aeterno adversarium, summo mollis timeam vel ad"]]

    fig = go.Figure(data=[go.Table(
        columnorder=[1, 2],
        columnwidth=[80, 400],
        header=dict(
            values=[['<b>EXPENSES</b><br>as of July 2017'],
                    ['<b>DESCRIPTION</b>']],
            line_color='darkslategray',
            fill_color='royalblue',
            align=['left', 'center'],
            font=dict(color='white', size=12),
            height=40
        ),
        cells=dict(
            values=values,
            line_color='darkslategray',
            fill=dict(color=['paleturquoise', 'white']),
            align=['left', 'center'],
            font_size=12,
            height=30)
    )
    ])
    fig.show()