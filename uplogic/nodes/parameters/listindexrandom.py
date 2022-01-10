from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid
import random


class ULListIndexRandom(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.condition = None
        self._item = None
        self.items = None
        self.OUT = ULOutSocket(self, self.get_val)

    def get_val(self):
        socket = self.get_output('val')
        if socket is None:
            list_d = self.get_input(self.items)
            if is_invalid(list_d):
                return STATUS_WAITING
            self._item = random.choice(list_d)
            return self.set_output('val', self._item)
        return socket

    def evaluate(self):
        self._set_ready()
