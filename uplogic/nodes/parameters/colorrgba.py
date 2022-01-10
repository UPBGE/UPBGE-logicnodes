from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import is_waiting


class ULColorRGBA(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.color = None
        self.output_vector = None
        self.OUTV = ULOutSocket(self, self.get_out_v)

    def get_out_v(self):
        socket = self.get_output('out_v')
        if socket is None:
            c = self.get_input(self.color)
            if is_waiting(c):
                return
            c = c.copy()
            c.resize_4d()
            return self.set_output('out_v', c)
        return socket

    def evaluate(self):
        self._set_ready()
