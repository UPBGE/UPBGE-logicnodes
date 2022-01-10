from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid


class ULGetParent(ULParameterNode):

    def __init__(self):
        ULParameterNode.__init__(self)
        self.game_object = None
        self.OUT = ULOutSocket(self, self.get_parent)

    def get_parent(self):
        game_object = self.get_input(self.game_object)
        if is_invalid(game_object):
            return STATUS_WAITING
        return game_object.parent

    def evaluate(self):
        self._set_ready()
