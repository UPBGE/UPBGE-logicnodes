from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import is_invalid


class ULObjectDataName(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.game_object = None
        self.OUT = ULOutSocket(self, self.get_name)

    def get_name(self):
        obj = self.get_socket_value(self.game_object)
        if is_invalid(obj):
            return
        self._set_value(obj.blenderObject.name)

    def evaluate(self):
        self._set_ready()
