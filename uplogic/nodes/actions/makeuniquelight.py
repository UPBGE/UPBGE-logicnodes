from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import make_unique_light
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULMakeUniqueLight(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.light = None
        self.done = None
        self._light = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.LIGHT = ULOutSocket(self, self.get_light)

    def get_done(self):
        return self.done

    def get_light(self):
        return self._light

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            self._set_value(False)
            return self._set_ready()
        old_lamp_ge = self.get_input(self.light)
        if is_waiting(old_lamp_ge):
            return
        self._set_ready()

        make_unique_light(old_lamp_ge)

        self.done = True
