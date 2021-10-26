from mathutils import Euler
from mathutils import Matrix
from mathutils import Vector
from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode


class ULEulerToMatrix(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.input_e = None
        self.matrix = Matrix()
        self.OUT = ULOutSocket(self, self.get_matrix)

    def get_matrix(self):
        vec = self.get_socket_value(self.input_e)
        if isinstance(vec, Vector):
            vec = Euler((vec.x, vec.y, vec.z), 'XYZ')
        return vec.to_matrix()

    def evaluate(self):
        self._set_ready()
