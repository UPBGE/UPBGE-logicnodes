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
        socket = self.get_output('matrix')
        if socket is None:
            vec = self.get_input(self.input_e)
            if isinstance(vec, Vector):
                vec = Euler((vec.x, vec.y, vec.z), 'XYZ')
            return self.set_output('matrix', vec.to_matrix())
        return socket

    def evaluate(self):
        self._set_ready()
