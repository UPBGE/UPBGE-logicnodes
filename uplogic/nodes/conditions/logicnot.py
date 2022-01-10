from uplogic.nodes import ULConditionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting


class ULNot(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.condition = None
        self.OUT = ULOutSocket(self, self.get_out)

    def get_out(self):
        socket = self.get_output('out')
        if socket is None:
            condition = self.get_input(self.condition)
            if is_waiting(condition):
                return STATUS_WAITING
            return self.set_output(
                'out',
                not condition
            )
        return socket

    def evaluate(self):
        self._set_ready()
