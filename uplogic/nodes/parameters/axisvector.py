from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import is_invalid
from uplogic.utils import LO_AXIS_TO_VECTOR


class ULAxisVector(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.game_object = None
        self.OUT = ULOutSocket(self, self.get_vec)

    def get_vec(self):
        obj = self.get_socket_value(self.game_object)
        front_vector = LO_AXIS_TO_VECTOR[self.axis]
        if is_invalid(obj, front_vector):
            return
        self._set_value(obj.getAxisVect(front_vector))

    def evaluate(self):
        self._set_ready()
