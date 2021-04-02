from SimComponents import QueueType
from StandardSimComponents import test_overloaded_switch, PacketGeneratorType

test_overloaded_switch(PacketGeneratorType.Bursty, QueueType.FIFO, 8)
