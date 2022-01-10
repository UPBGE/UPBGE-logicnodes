from uplogic.nodes import ULConditionNode


class ULOnNextTick(ULConditionNode):

    def __init__(self):
        ULConditionNode.__init__(self)
        self.input_condition = None
        self._activated = 0

    def evaluate(self):
        input_condition = self.get_input(self.input_condition)
        self._set_ready()
        if self._activated == 1:
            self._set_value(True)
            if not input_condition:
                self._activated = 0
        elif input_condition:
            self._set_value(False)
            self._activated = 1
        elif self._activated == 0:
            self._set_value(False)
