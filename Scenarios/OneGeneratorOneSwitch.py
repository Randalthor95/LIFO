from DataGeneration import print_metrics
from SimComponents import QueueType
from StandardSimComponents import test_one_generator_one_switch, PacketGeneratorType, test_one_generator_one_switch_all

# test_one_generator_one_switch_all(PacketGeneratorType.Constant)
# test_one_generator_one_switch_all(PacketGeneratorType.Bursty)
# test_one_generator_one_switch_all(PacketGeneratorType.Exponential)
# test_one_generator_one_switch_all(PacketGeneratorType.Normal)

result = test_one_generator_one_switch(PacketGeneratorType.Bursty, QueueType.FIFO)
print_metrics('One_Generator_One_Switch', QueueType.FIFO, result.packet_generators, result.packet_sink,
              result.switch_ports, result.port_monitors, 200)
