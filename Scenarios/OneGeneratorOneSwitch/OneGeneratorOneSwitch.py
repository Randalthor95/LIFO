from SimComponents import QueueType
from StandardSimComponents import test_one_generator_one_switch, PacketGeneratorType

# test_one_generator_one_switch(PacketGeneratorType.Constant, QueueType.FIFO)
#test_one_generator_one_switch(PacketGeneratorType.Bursty, QueueType.FIFO)
test_one_generator_one_switch(PacketGeneratorType.Normal, QueueType.FIFO)
# test_one_generator_one_switch(PacketGeneratorType.Exponential, QueueType.FIFO)
