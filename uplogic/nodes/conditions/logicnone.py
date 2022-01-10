from uplogic.nodes import ULConditionNode


class ULNone(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.checked_value = None

    def evaluate(self):
        self._set_ready()
        value = self.get_input(self.checked_value)
        self._set_value(value is None)
