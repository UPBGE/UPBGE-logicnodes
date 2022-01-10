from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULSetCurvePoints(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.curve_object = None
        self.points: list = None
        self.done: bool = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        curve_object = self.get_input(self.curve_object)
        points = self.get_input(self.points)
        if is_waiting(points):
            return
        if is_invalid(curve_object):
            return
        self._set_ready()
        if not points:
            return
        curve = curve_object.blenderObject.data
        for spline in curve.splines:
            curve.splines.remove(spline)
        spline = curve.splines.new('NURBS')
        pos = curve_object.worldPosition
        spline.points.add(len(points))
        for p, new_co in zip(spline.points, points):
            p.co = ([
                new_co.x - pos.x,
                new_co.y - pos.y,
                new_co.z - pos.z
            ] + [1.0])
        self.done = True
