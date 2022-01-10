from uplogic.nodes import ULConditionNode
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULTimer(ULConditionNode):

    def __init__(self):
        ULConditionNode.__init__(self)
        self.condition = None
        self.delta_time = None
        self._trigger = -1
        self.network = None

    def setup(self, network):
        self.network = network

    def evaluate(self):
        condition = self.get_input(self.condition)
        delta_time = self.get_input(self.delta_time)
        if is_waiting(delta_time):
            return
        self._set_ready()
        now = self.network.timeline

        if not not_met(condition):
            self._trigger = now + delta_time

        if self._trigger == -1 or now < self._trigger:
            self._set_value(False)
        else:
            self._set_value(True)
            self._trigger = -1
