from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting


class ULTypeCastValue(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.value = None
        self.to_type = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        value = self.get_input(self.value)
        to_type = self.get_input(self.to_type)
        if is_waiting(to_type, value):
            return STATUS_WAITING
        return self.typecast_value(value, to_type)

    def evaluate(self):
        self._set_ready()

    def typecast_value(self, value, t):
        if t == 'int':
            return int(value)
        elif t == 'bool':
            return bool(value)
        elif t == 'str':
            return str(value)
        elif t == 'float':
            return float(value)
        return value
