from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import LO_AXIS_TO_VECTOR
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid


class ULAxisVector(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.game_object = None
        self.OUT = ULOutSocket(self, self.get_vec)

    def get_vec(self):
        socket = self.get_output('vec')
        if socket is None:
            obj = self.get_input(self.game_object)
            front_vector = LO_AXIS_TO_VECTOR[self.axis]
            if is_invalid(obj, front_vector):
                return STATUS_WAITING
            return self.set_output(
                'vec',
                obj.getAxisVect(front_vector)
            )
        return socket

    def evaluate(self):
        self._set_ready()
