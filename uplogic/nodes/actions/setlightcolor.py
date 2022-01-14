from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULSetLightColor(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.lamp = None
        self.color = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            self._set_value(False)
            return self._set_ready()
        lamp = self.get_input(self.lamp)
        color = self.get_input(self.color)
        if is_waiting(lamp, color):
            return
        if len(color) > 3:
            color = color[:-1]
        self._set_ready()
        light = lamp.blenderObject.data
        light.color = color
        self.done = True
