from mathutils import Vector
from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import is_invalid


class ULVectorSplitXY(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.input_v = None
        self.output_v = Vector()
        self.OUTX = ULOutSocket(self, self.get_out_x)
        self.OUTY = ULOutSocket(self, self.get_out_y)

    def get_out_x(self):
        return self.output_v.x

    def get_out_y(self):
        return self.output_v.y

    def evaluate(self):
        self._set_ready()
        vec = self.get_input(self.input_v)
        if not is_invalid(vec):
            self.output_v = vec
