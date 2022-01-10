from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting


class ULListFromItems(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.value = None
        self.value2 = None
        self.value3 = None
        self.value4 = None
        self.value5 = None
        self.value6 = None
        self.items: list = None
        self.LIST = ULOutSocket(self, self.get_list)

    def get_list(self):
        socket = self.get_output('list')
        if socket is None:
            value = self.get_input(self.value)
            value2 = self.get_input(self.value2)
            value3 = self.get_input(self.value3)
            value4 = self.get_input(self.value4)
            value5 = self.get_input(self.value5)
            value6 = self.get_input(self.value6)
            values = [value, value2, value3, value4, value5, value6]
            self.items = []
            for val in values:
                if not is_waiting(val) and not is_invalid(val):
                    self.items.append(val)
            return self.set_output('list', self.items)
        return socket

    def evaluate(self):
        self._set_ready()
