

from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import is_waiting


class ULInitEmptyList(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.condition = None
        self.length = None
        self.items = None
        self.LIST = ULOutSocket(self, self.get_list)

    def get_list(self):
        length = self.get_input(self.length)
        if is_waiting(length):
            return
        return [None for x in range(length)]

    def evaluate(self):
        self._set_ready()
