from uplogic.nodes import GEConditionNode


class GEOnNextFrame(GEConditionNode):

    def __init__(self):
        super()
        self.input_condition = None
        self._activated = 0

    def evaluate(self):
        input_condition = self.get_socket_value(self.input_condition)
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
