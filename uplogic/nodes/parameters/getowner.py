from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_READY


class ULGetOwner(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)

    def setup(self, network):
        ULParameterNode.setup(self, network)
        self._set_status(STATUS_READY)
        self._set_value(network.get_owner())

    def reset(self):
        pass

    def evaluate(self):
        pass
