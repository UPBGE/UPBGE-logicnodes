from bge import logic
from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode


class ULGetGravity(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.collection = None
        self.OUT = ULOutSocket(self, self.get_gravity)

    def get_gravity(self):
        return logic.getCurrentScene().gravity

    def evaluate(self):
        self._set_ready()
