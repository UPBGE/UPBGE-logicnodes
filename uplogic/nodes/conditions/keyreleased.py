from uplogic.nodes import ULConditionNode
from uplogic.utils import is_waiting


class ULKeyReleased(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.pulse = False
        self.key_code = None
        self.network = None

    def setup(self, network):
        self.network = network

    def evaluate(self):
        keycode = self.get_input(self.key_code)
        if is_waiting(keycode):
            return
        self._set_ready()
        keystat = self.network.keyboard_events[keycode]
        if self.pulse:
            self._set_value(
                keystat.released or
                keystat.inactive
            )
        else:
            self._set_value(keystat.released)
