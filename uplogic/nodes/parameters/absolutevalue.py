from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid
import math


class ULAbsoluteValue(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.value = None
        self.out_value = False
        self.OUT = ULOutSocket(self, self._get_out_value)

    def _get_out_value(self):
        value = self.get_input(self.value)
        if is_invalid(self.value):
            return STATUS_WAITING
        return math.fabs(value)

    def evaluate(self):
        self._set_ready()
