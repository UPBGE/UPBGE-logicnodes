from mathutils import Vector
from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING, is_invalid


class ULVectorAbsolute(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.input_v = None
        self.output_v = Vector()
        self.OUTV = ULOutSocket(self, self.get_out_v)

    def get_out_v(self):
        vec = self.get_input(self.input_v)
        if is_invalid(vec):
            return STATUS_WAITING
        vec = vec.copy()
        vec.x = abs(vec.x)
        vec.y = abs(vec.y)
        vec.z = abs(vec.z)
        return vec

    def evaluate(self):
        self._set_ready()
