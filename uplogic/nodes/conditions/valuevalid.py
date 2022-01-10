from uplogic.nodes import ULConditionNode
from uplogic.utils import is_invalid


class ULValueValid(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.checked_value = None

    def evaluate(self):
        self._set_ready()
        value = self.get_input(self.checked_value)
        self._set_value(not is_invalid(value))
