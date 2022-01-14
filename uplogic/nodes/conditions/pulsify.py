from uplogic.nodes import ULConditionNode
from uplogic.utils import is_waiting


class ULPulsify(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.condition = None
        self.delay = None
        self._triggered = False
        self._triggered_time = None
        self._trigger_delay = None

    def evaluate(self):
        socket = self.get_output('out')
        if socket is None:
            if self._triggered is True:
                self._set_ready()
                delta = self.network.timeline - self._triggered_time
                if delta < self._trigger_delay:
                    self._set_value(False)
                    return self.set_output('out', False)
            condition = self.get_input(self.condition)
            delay = self.get_input(self.delay)
            if is_waiting(condition, delay):
                return self.set_output('out', False)
            self._set_ready()
            self._set_value(False)
            if delay is None:
                return self.set_output('out', False)
            if condition is None:
                return self.set_output('out', False)
            if condition:
                self._triggered = True
                self._triggered_time = self.network.timeline
                self._trigger_delay = delay
                self._set_value(True)
                return self.set_output('out', True)
        return socket
