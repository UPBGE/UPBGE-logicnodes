from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket


class ULSimpleValue(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.value = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        value = self.get_input(self.value)
        return value

    def evaluate(self):
        self._set_ready()
