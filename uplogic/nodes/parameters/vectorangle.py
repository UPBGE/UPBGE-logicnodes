from mathutils import Vector
from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid
import math


class ULVectorAngle(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.op = None
        self.vector: Vector = None
        self.vector_2: Vector = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        vector: Vector = self.get_input(self.vector)
        vector_2: Vector = self.get_input(self.vector_2)
        if is_invalid(
            vector,
            vector_2
        ):
            return STATUS_WAITING
        rad: float = vector.angle(vector_2)
        deg: float = rad * 180/math.pi
        return deg

    def evaluate(self):
        self._set_ready()
