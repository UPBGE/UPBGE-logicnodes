from mathutils import Vector
from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import is_invalid


class ULGetCurvePoints(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.curve = None
        self.OUT = ULOutSocket(self, self.get_points)

    def get_points(self):
        obj = self.get_socket_value(self.curve)
        if is_invalid(obj):
            return
        offset = obj.worldPosition
        o = obj.blenderObject.data.splines[0]
        if o.type == 'BEZIER':
            return [Vector(p.co) + offset for p in o.bezier_points]
        return [Vector(p.co[:-1]) + offset for p in o.points]

    def evaluate(self):
        self._set_ready()
