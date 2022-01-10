from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid


class ULVectorMath(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.op = None
        self.vector = None
        self.vector_2 = None
        self.factor = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        op = self.get_input(self.op)
        vector = self.get_input(self.vector)
        vector_2 = self.get_input(self.vector_2)
        factor = self.get_input(self.factor)
        if is_waiting(
            op,
            factor
        ):
            return STATUS_WAITING
        if is_invalid(
            vector,
            vector_2
        ):
            return STATUS_WAITING
        return self.calc_output_vector(op, vector, vector_2, factor)

    def evaluate(self):
        self._set_ready()

    def calc_output_vector(self, op, vec, vec2, fac):
        matvec = vec.copy()
        if op == 'normalize':
            matvec.normalize()
        elif op == 'lerp':
            return matvec.lerp(vec2, fac)
        elif op == 'negate':
            matvec.negate()
        elif op == 'dot':
            return matvec.dot(vec2)
        elif op == 'cross':
            return matvec.cross(vec2)
        elif op == 'project':
            return matvec.project(vec2)
        return matvec
