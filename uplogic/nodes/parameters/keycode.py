from uplogic.nodes import GEParameterNode


class GEKeyCode(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.key_code = None

    def evaluate(self):
        self._set_ready()
        key_code = self.get_socket_value(self.key_code)
        self._set_value(key_code)
