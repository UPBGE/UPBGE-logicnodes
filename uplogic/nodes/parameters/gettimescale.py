from bge import logic
from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket


class ULGetTimeScale(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return logic.getTimeScale()

    def evaluate(self):
        self._set_ready()
