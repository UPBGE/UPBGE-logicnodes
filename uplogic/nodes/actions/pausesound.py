from uplogic.nodes import ULActionNode
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULPauseSound(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.sound = None

    def evaluate(self):
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        sound = self.get_input(self.sound)
        if is_waiting(sound):
            return
        self._set_ready()
        if sound is None:
            return
        sound.pause()
        self._set_value(True)
