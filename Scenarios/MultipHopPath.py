from SimComponents import QueueType
from StandardSimComponents import test_multihop_path, PacketGeneratorType

test_multihop_path(PacketGeneratorType.Normal, QueueType.FIFO, 9)
