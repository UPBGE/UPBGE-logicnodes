from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULSetLightShadow(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.lamp = None
        self.use_shadow = None
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
        use_shadow = self.get_input(self.use_shadow)
        if is_waiting(lamp, use_shadow):
            return
        self._set_ready()
        light = lamp.blenderObject.data
        light.use_shadow = use_shadow
        self.done = True
