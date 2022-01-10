from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import is_invalid


class ULDictValue(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.dict = None
        self.key = None
        self.OUT = ULOutSocket(self, self.get_val)

    def get_val(self):
        socket = self.get_output('val')
        if socket is None:
            dictionary = self.get_input(self.dict)
            key = self.get_input(self.key)
            if is_invalid(dictionary, key):
                return
            return self.set_output('val', dictionary.get(key))
        return socket

    def evaluate(self):
        self._set_ready()
