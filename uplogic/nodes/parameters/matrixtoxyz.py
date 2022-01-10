from mathutils import Euler
from mathutils import Vector
from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode


class ULMatrixToXYZ(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.input_m = None
        self.output = None
        self.euler = Euler()
        self.OUT = ULOutSocket(self, self.get_out)

    def get_out(self):
        matrix = self.get_input(self.input_m)
        if self.output:
            return matrix.to_euler()
        else:
            e = matrix.to_euler()
            return Vector((e.x, e.y, e.z))

    def evaluate(self):
        self._set_ready()
