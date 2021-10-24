from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting


class ULRangedThreshold(ULParameterNode):

    @classmethod
    def op_by_code(cls, op):
        return op

    def __init__(self):
        ULParameterNode.__init__(self)
        self.value = None
        self.threshold = None
        self.operator = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        v = self.get_socket_value(self.value)
        t = self.get_socket_value(self.threshold)
        if is_waiting(v, t):
            return STATUS_WAITING
        value = self.calc_threshold(self.operator, v, t)
        if (v is None) or (t is None):
            return STATUS_WAITING
        else:
            return value

    def calc_threshold(self, op, v, t):
        if op == 'OUTSIDE':
            return v if (v < t.x or v > t.y) else 0
        if op == 'INSIDE':
            return v if (t.x < v < t.y) else 0

    def evaluate(self):
        self._set_ready()
