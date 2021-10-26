from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting
from uplogic.utils import compute_distance


class ULDistance(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.parama = None
        self.paramb = None
        self.OUT = ULOutSocket(self, self.get_out)

    def get_out(self):
        parama = self.get_socket_value(self.parama)
        paramb = self.get_socket_value(self.paramb)
        if is_waiting(parama, paramb):
            return STATUS_WAITING
        return compute_distance(parama, paramb)

    def evaluate(self):
        self._set_ready()
