from uplogic.nodes import ULConditionNode
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULDelay(ULConditionNode):
    consumed: bool
    triggers: list

    def __init__(self):
        ULConditionNode.__init__(self)
        self.condition = None
        self.delay = None
        self.triggers = []

    def evaluate(self):
        condition = self.get_input(self.condition)
        delay = self.get_input(self.delay)
        if is_invalid(delay):
            return
        self._set_ready()

        now = self.network.timeline

        if not not_met(condition):
            self.triggers.append(now + delay)

        if not self.triggers:
            self._set_value(False)
            return
        t = self.triggers[0]
        if now >= t:
            self._set_value(True)
            self.triggers.remove(t)
            return
        self._set_value(False)
