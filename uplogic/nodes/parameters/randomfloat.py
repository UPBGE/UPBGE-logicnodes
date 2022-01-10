from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting
import sys
import random


class ULRandomFloat(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.max_value = None
        self.min_value = None
        self.OUT_A = ULOutSocket(self, self._get_output)

    def _get_output(self):
        socket = self.get_output('output')
        if socket is None:
            min_value = self.get_input(self.min_value)
            max_value = self.get_input(self.max_value)
            if is_waiting(min_value, max_value):
                return STATUS_WAITING
            if min_value > max_value:
                min_value, max_value = max_value, min_value
            if min_value == max_value:
                min_value = sys.float_info.min
                max_value = sys.float_info.max

            delta = max_value - min_value
            return self.set_output(
                'output',
                min_value + (delta * random.random())
            )
        return socket

    def evaluate(self):
        self._set_ready()
