from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import interpolate
from uplogic.utils import is_invalid


class ULInterpolate(ULParameterNode):

    def __init__(self):
        ULParameterNode.__init__(self)
        self.a = None
        self.b = None
        self.fac = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        a = self.get_socket_value(self.a)
        b = self.get_socket_value(self.b)
        fac = self.get_socket_value(self.fac)
        if is_invalid(a, b, fac):
            return STATUS_WAITING
        return interpolate(a, b, fac)

    def evaluate(self):
        self._set_ready()
