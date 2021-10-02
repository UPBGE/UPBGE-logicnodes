from uplogic.nodes import GEParameterNode
from uplogic.nodes import STATUS_READY


class GEGetOwner(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)

    def setup(self, network):
        GEParameterNode.setup(self, network)
        self._set_status(STATUS_READY)
        self._set_value(network.get_owner())

    def reset(self):
        pass

    def evaluate(self):
        pass
