from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting


class ULGetLightColor(ULParameterNode):

    def __init__(self):
        ULParameterNode.__init__(self)
        self.lamp = None
        self.color = 0
        self.COLOR = ULOutSocket(self, self.get_color)

    def get_color(self):
        lamp = self.get_input(self.lamp)
        if is_waiting(lamp):
            return STATUS_WAITING
        light = lamp.blenderObject.data
        return light.color

    def evaluate(self):
        self._set_ready()
