from mathutils import Vector
from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid


class ULMath(ULParameterNode):

    @classmethod
    def op_by_code(cls, str):
        import operator
        opmap = {
            "ADD": operator.add,
            "SUB": operator.sub,
            "DIV": operator.truediv,
            "MUL": operator.mul
        }
        return opmap.get(str)

    def __init__(self):
        ULParameterNode.__init__(self)
        self.operand_a = None
        self.operand_b = None
        self.operator = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        socket = self.get_socket('done')
        if socket is None:
            a = self.get_socket_value(self.operand_a)
            b = self.get_socket_value(self.operand_b)
            if is_invalid(a, b):
                return STATUS_WAITING
            if (a is None) or (b is None):
                return STATUS_WAITING
            else:
                if (
                    isinstance(a, Vector) and
                    isinstance(b, Vector)
                ):
                    return self.get_vec_vec_calc(a, b)
                elif isinstance(a, Vector):
                    return self.get_vec_calc(a, b)
                elif isinstance(b, Vector):
                    return self.get_vec_calc(b, a)
                return self.set_socket('done', self.operator(a, b))
        return socket

    def evaluate(self):
        self._set_ready()

    def get_vec_calc(self, vec, num):
        if len(vec) == 4:
            return Vector(
                (
                    self.operator(vec.x, num),
                    self.operator(vec.y, num),
                    self.operator(vec.z, num),
                    self.operator(vec.w, num)
                )
            )
        else:
            return Vector(
                (
                    self.operator(vec.x, num),
                    self.operator(vec.y, num),
                    self.operator(vec.z, num)
                )
            )

    def get_vec_vec_calc(self, vec, vec2):
        if len(vec) == 4 and len(vec2) == 4:
            return Vector(
                (
                    self.operator(vec.x, vec2.x),
                    self.operator(vec.y, vec2.y),
                    self.operator(vec.z, vec2.z),
                    self.operator(vec.w, vec2.w)
                )
            )
        else:
            return Vector(
                (
                    self.operator(vec.x, vec2.x),
                    self.operator(vec.y, vec2.y),
                    self.operator(vec.z, vec2.z)
                )
            )
