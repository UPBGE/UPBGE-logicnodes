from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid


class ULClamp(ULParameterNode):

    def __init__(self):
        ULParameterNode.__init__(self)
        self.value = None
        self.range = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        socket = self.get_output('result')
        if socket is None:
            value = self.get_input(self.value)
            range_ft = self.get_input(self.range)
            if is_waiting(range_ft):
                return STATUS_WAITING
            if is_invalid(value):
                return STATUS_WAITING
            if range_ft.x == range_ft.y:
                return value
            if value < range_ft.x:
                value = range_ft.x
            if value > range_ft.y:
                value = range_ft.y
            return self.set_output('result', value)
        return socket

    def evaluate(self):
        self._set_ready()
