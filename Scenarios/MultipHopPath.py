from SimComponents import QueueType
from StandardSimComponents import test_multihop_path, PacketGeneratorType, test_multihop_path_all

test_multihop_path_all(PacketGeneratorType.Constant, 9)
test_multihop_path_all(PacketGeneratorType.Bursty, 9)
test_multihop_path_all(PacketGeneratorType.Normal, 9)
test_multihop_path_all(PacketGeneratorType.Exponential, 9)
