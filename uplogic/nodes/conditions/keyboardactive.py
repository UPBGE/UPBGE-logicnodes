from uplogic.nodes import ULConditionNode


class ULKeyboardActive(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)

    def evaluate(self):
        self._set_ready()
        self._set_value(
            len(self.network.active_keyboard_events) > 0
        )
