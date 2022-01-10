from uplogic.nodes import ULConditionNode
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULOnce(ULConditionNode):

    def __init__(self):
        ULConditionNode.__init__(self)
        self.input_condition = None
        self.repeat = None
        self.reset_time = None
        self._consumed = False
        self.time = 0.0

    def evaluate(self):
        condition = self.get_input(self.input_condition)
        repeat = self.get_input(self.repeat)
        reset_time = self.get_input(self.reset_time)
        if is_waiting(repeat, reset_time):
            self._set_value(False)
            return
        network = self.network
        tl = network.timeline

        self._set_ready()
        cond_f = not_met(condition)
        self.time = tl
        if not cond_f and self._consumed is False:
            self._consumed = True
            self._set_value(True)
            return
        if cond_f and repeat and self._consumed:
            self._consumed = False
        self._set_value(False)
