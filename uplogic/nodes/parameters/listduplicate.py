from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid


class ULListDuplicate(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.condition = None
        self.items = None
        self.OUT = ULOutSocket(self, self.get_points)

    def get_points(self):
        list_d = self.get_socket_value(self.items)
        if is_invalid(list_d):
            return STATUS_WAITING
        self._set_value(list_d.copy())

    def evaluate(self):
        self._set_ready()
