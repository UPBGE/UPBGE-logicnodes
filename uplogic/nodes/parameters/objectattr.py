from mathutils import Vector
from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid


class ULObjectAttribute(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.game_object = None
        self.attribute_name = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        game_object = self.get_input(self.game_object)
        attribute_name = self.get_input(self.attribute_name)
        if is_waiting(game_object, attribute_name):
            return STATUS_WAITING
        if is_invalid(game_object):
            return STATUS_WAITING
        if not hasattr(game_object, attribute_name):
            return STATUS_WAITING
        val = getattr(game_object, attribute_name)
        return val.copy() if isinstance(val, Vector) else val

    def evaluate(self):
        self._set_ready()
