from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid


class ULInvertValue(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.value = None
        self.out_value = False
        self.OUT = ULOutSocket(self, self._get_out_value)

    def _get_out_value(self):
        value = self.get_input(self.value)
        if is_invalid(value):
            self.out_value = 0
            return
        return not value if type(value) is str else -value

    def evaluate(self):
        self._set_ready()
