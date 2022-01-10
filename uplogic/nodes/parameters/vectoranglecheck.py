from mathutils import Vector
from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import LOGIC_OPERATORS
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
import math


class ULVectorAngleCheck(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.op: str = None
        self.vector: Vector = None
        self.vector_2: Vector = None
        self.value = None
        self._angle = 0
        self.OUT = ULOutSocket(self, self.get_done)
        self.ANGLE = ULOutSocket(self, self.get_angle)

    def get_angle(self):
        return self._angle

    def get_done(self):
        op: str = self.get_input(self.op)
        if is_waiting(
            op
        ):
            return STATUS_WAITING
        value: float = self.get_input(self.value)
        return LOGIC_OPERATORS[int(op)](self._angle, value)

    def evaluate(self):
        vector: Vector = self.get_input(self.vector)
        vector_2: Vector = self.get_input(self.vector_2)
        if is_invalid(
            vector,
            vector_2
        ):
            return
        self._set_ready()
        rad: float = vector.angle(vector_2)
        deg: float = rad * 180/math.pi
        self._angle = deg
