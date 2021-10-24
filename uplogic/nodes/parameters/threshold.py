from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid


class ULThreshold(ULParameterNode):

    @classmethod
    def op_by_code(cls, op):
        return op

    def __init__(self):
        ULParameterNode.__init__(self)
        self.value = None
        self.else_z = None
        self.threshold = None
        self.operator = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        v = self.get_socket_value(self.value)
        e = self.get_socket_value(self.else_z)
        t = self.get_socket_value(self.threshold)
        if is_invalid(v, t):
            return STATUS_WAITING
        value = self.calc_threshold(self.operator, v, t, e)
        if (v is None) or (t is None):
            return STATUS_WAITING
        else:
            return value

    def evaluate(self):
        self._set_ready()

    def calc_threshold(self, op, v, t, e):
        if op == 'GREATER':
            return v if v > t else (0 if e else t)
        if op == 'LESS':
            return v if v < t else (0 if e else t)
