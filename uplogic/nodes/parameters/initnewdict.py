from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting


class ULInitNewDict(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.key = None
        self.val = None
        self.DICT = ULOutSocket(self, self.get_dict)

    def get_dict(self):
        key = self.get_input(self.key)
        value = self.get_input(self.val)
        if is_waiting(key, value):
            return STATUS_WAITING
        return {str(key): value}

    def evaluate(self):
        self._set_ready()
