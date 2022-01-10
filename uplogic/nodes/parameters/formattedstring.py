from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid


class ULFormattedString(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.format_string = None
        self.value_a = None
        self.value_b = None
        self.value_c = None
        self.value_d = None
        self.OUT = ULOutSocket(self, self.get_out)

    def get_out(self):
        socket = self.get_output('out')
        if socket is None:
            format_string = self.get_input(self.format_string)
            value_a = self.get_input(self.value_a)
            value_b = self.get_input(self.value_b)
            value_c = self.get_input(self.value_c)
            value_d = self.get_input(self.value_d)
            if is_invalid(format_string):
                return STATUS_WAITING
            if is_waiting(value_a, value_b, value_c, value_d):
                return STATUS_WAITING
            result = format_string.format(value_a, value_b, value_c, value_d)
            return self.set_output('out', result)
        return socket

    def evaluate(self):
        self._set_ready()
