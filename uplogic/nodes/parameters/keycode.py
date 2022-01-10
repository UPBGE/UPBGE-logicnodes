from uplogic.nodes import ULParameterNode


class ULKeyCode(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.key_code = None

    def evaluate(self):
        self._set_ready()
        key_code = self.get_input(self.key_code)
        self._set_value(key_code)
