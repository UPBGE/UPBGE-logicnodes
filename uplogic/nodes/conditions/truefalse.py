from uplogic.nodes import ULConditionNode
from uplogic.nodes import ULOutSocket


class ULTrueFalse(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.state = None
        self.TRUE = ULOutSocket(self, self.get_true_value)
        self.FALSE = ULOutSocket(self, self.get_false_value)

    def get_true_value(self):
        return self.get_input(self.state)

    def get_false_value(self):
        return not self.get_input(self.state)

    def evaluate(self):
        self._set_ready()
