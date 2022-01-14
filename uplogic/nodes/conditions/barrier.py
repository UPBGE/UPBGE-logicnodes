from uplogic.nodes import ULConditionNode
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULBarrier(ULConditionNode):
    consumed: bool
    trigger: float

    def __init__(self):
        ULConditionNode.__init__(self)
        self.condition = None
        self.time = None
        self.consumed = False
        self.trigger = 0

    def evaluate(self):
        condition = self.get_input(self.condition)
        time = self.get_input(self.time)
        if is_waiting(time):
            return

        self._set_ready()

        now = self.network.timeline

        if not not_met(condition):
            if not self.consumed:
                self.consumed = True
                self.trigger = now + time

            if now >= self.trigger:
                self._set_value(True)

        else:
            self._set_value(False)
            self.consumed = False
