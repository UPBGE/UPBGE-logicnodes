from bge import render
from uplogic.nodes import ULActionNode
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULDrawLine(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.color = None
        self.from_point = None
        self.to_point = None

    def evaluate(self):
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        from_point = self.get_input(self.from_point)
        to_point = self.get_input(self.to_point)
        color = self.get_input(self.color)
        if is_invalid(from_point, to_point, color):
            return
        self._set_ready()
        render.drawLine(
            from_point,
            to_point,
            [
                color.x,
                color.y,
                color.z,
                1
            ]
        )
        self._set_value(True)
