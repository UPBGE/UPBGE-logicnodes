from mathutils import Vector
from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting


class ULLimitRange(ULParameterNode):

    @classmethod
    def op_by_code(cls, op):
        return op

    def __init__(self):
        ULParameterNode.__init__(self)
        self.value = None
        self.threshold = Vector((0, 0))
        self.operator = None
        self.last_val = 0
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        socket = self.get_output('done')
        if socket is None:
            v = self.get_input(self.value)
            t = self.get_input(self.threshold)
            if is_waiting(v, t):
                return STATUS_WAITING
            self.calc_threshold(self.operator, v, t)
            if (v is None) or (t is None):
                return STATUS_WAITING
            else:
                return self.set_output('done', self.last_val)
        return socket

    def calc_threshold(self, op, v, t):
        last = self.last_val
        if op == 'OUTSIDE':
            if (v < t.x or v > t.y):
                self.last_val = v
            else:
                self.last_val = t.x if last <= t.x else t.y
        if op == 'INSIDE':
            if (t.x < v < t.y):
                self.last_val = v
            else:
                self.last_val = t.x if v <= t.x else t.y

    def evaluate(self):
        self._set_ready()
