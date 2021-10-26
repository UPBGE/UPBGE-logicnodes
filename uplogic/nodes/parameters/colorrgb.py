from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import is_waiting


class ULColorRGB(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.color = None
        self.output_vector = None
        self.OUTV = ULOutSocket(self, self.get_out_v)

    def get_out_v(self):
        c = self.get_socket_value(self.color)
        if is_waiting(c):
            return
        return c.copy()

    def evaluate(self):
        self._set_ready()
