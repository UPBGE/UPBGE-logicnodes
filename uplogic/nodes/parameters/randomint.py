

from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting
import random
import sys


class ULRandomInt(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.max_value = None
        self.min_value = None
        self.OUT_A = ULOutSocket(self, self._get_output)

    def _get_output(self):
        socket = self.get_output('result')
        if socket is None:
            min_value = self.get_input(self.min_value)
            max_value = self.get_input(self.max_value)
            if is_waiting(max_value, min_value):
                return STATUS_WAITING
            if min_value > max_value:
                min_value, max_value = max_value, min_value
            if min_value == max_value:
                min_value = -sys.maxsize
                max_value = sys.maxsize

            return self.set_output(
                'result',
                random.randint(min_value, max_value)
            )
        return socket

    def evaluate(self):
        self._set_ready()
