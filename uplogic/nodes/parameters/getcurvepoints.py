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
        socket = self.get_output('points')
        if socket is None:
            obj = self.get_input(self.curve)
            if is_invalid(obj):
                return
            offset = obj.worldPosition
            o = obj.blenderObject.data.splines[0]
            if o.type == 'BEZIER':
                return self.set_output(
                    'points',
                    [Vector(p.co) + offset for p in o.bezier_points]
                )
            return self.set_output(
                'points',
                [Vector(p.co[:-1]) + offset for p in o.points]
            )
        return socket

    def evaluate(self):
        self._set_ready()
