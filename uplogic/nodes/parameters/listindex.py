from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting


class ULListIndex(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.items = None
        self.index = None
        self.OUT = ULOutSocket(self, self.get_val)

    def get_val(self):
        list_d = self.get_input(self.items)
        index = self.get_input(self.index)
        if is_invalid(list_d):
            return STATUS_WAITING
        if is_waiting(index):
            return STATUS_WAITING
        if index <= len(list_d) - 1:
            return list_d[index]
        return STATUS_WAITING

    def evaluate(self):
        self._set_ready()
