from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid


class ULGetSound(ULParameterNode):

    def __init__(self):
        ULParameterNode.__init__(self)
        self.sound = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        sound = self.get_input(self.sound)
        if is_invalid(sound):
            return STATUS_WAITING
        return sound

    def evaluate(self):
        self._set_ready()
