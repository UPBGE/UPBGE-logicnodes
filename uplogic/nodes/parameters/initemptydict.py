from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode


class ULInitEmptyDict(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.condition = None
        self.dict = None
        self.done = None
        self.DICT = ULOutSocket(self, self.get_dict)

    def get_dict(self):
        return {}

    def evaluate(self):
        self._set_ready()
