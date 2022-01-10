from uplogic.nodes import ULConditionNode


class ULNotNone(ULConditionNode):

    def __init__(self):
        ULConditionNode.__init__(self)
        self.checked_value = None

    def evaluate(self):
        value = self.get_input(self.checked_value)
        self._set_ready()
        self._set_value(value is not None)
