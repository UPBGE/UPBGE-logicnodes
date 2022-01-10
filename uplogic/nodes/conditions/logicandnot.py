from uplogic.nodes import ULConditionNode
from uplogic.utils import is_waiting


class ULAndNot(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.condition_a = None
        self.condition_b = None

    def evaluate(self):
        ca = self.get_input(self.condition_a)
        cb = not self.get_input(self.condition_b)
        self._set_ready()
        if is_waiting(ca, cb):
            self._set_value(False)
            return
        self._set_value(ca and cb)
