from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting


class ULWithinRange(ULParameterNode):

    @classmethod
    def op_by_code(cls, op):
        return op

    def __init__(self):
        ULParameterNode.__init__(self)
        self.value = None
        self.range = None
        self.operator = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        v = self.get_input(self.value)
        r = self.get_input(self.range)
        if is_waiting(v, r):
            return STATUS_WAITING
        value = self.calc_range(self.operator, v, r)
        if (v is None) or (r is None):
            return STATUS_WAITING
        else:
            return value

    def calc_range(self, op, v, r):
        if op == 'OUTSIDE':
            return True if (v < r.x or v > r.y) else False
        if op == 'INSIDE':
            return True if (r.x < v < r.y) else False

    def evaluate(self):
        self._set_ready()
