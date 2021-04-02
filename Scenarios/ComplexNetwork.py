from SimComponents import QueueType
from StandardSimComponents import PacketGeneratorType, test_complex_network

test_complex_network(PacketGeneratorType.Normal, QueueType.FIFO)
