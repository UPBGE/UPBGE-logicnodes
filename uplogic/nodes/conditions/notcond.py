from uplogic.nodes import ULConditionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting


class ULNot(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.condition = None
        self.OUT = ULOutSocket(self, self.get_out)

    def get_out(self):
        condition = self.get_socket_value(self.condition)
        if is_waiting(condition):
            return
        return not condition

    def evaluate(self):
        self._set_ready()
