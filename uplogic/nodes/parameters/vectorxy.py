from mathutils import Vector
from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import is_invalid


class ULVectorXY(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.input_x = None
        self.input_y = None
        self.OUTV = ULOutSocket(self, self.get_out_v)

    def get_out_v(self):
        x = self.get_input(self.input_x)
        y = self.get_input(self.input_y)
        v = Vector((0, 0, 0))
        if not is_invalid(x):
            v.x = x
        if not is_invalid(y):
            v.y = y
        return v.copy()

    def evaluate(self):
        self._set_ready()
