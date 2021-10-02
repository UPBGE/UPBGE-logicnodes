from uplogic.nodes import GEConditionNode


class GEKeyboardActive(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)

    def evaluate(self):
        self._set_ready()
        self._set_value(
            len(self.network.active_keyboard_events) > 0
        )
