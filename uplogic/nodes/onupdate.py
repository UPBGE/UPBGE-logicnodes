from uplogic.nodes import GEConditionNode
from uplogic.nodes import STATUS_READY


class GEOnUpdate(GEConditionNode):
    def __init__(self):
        super()
        self._set_status(STATUS_READY)
        self._value = True

    def reset(self):
        self._value = True

    def evaluate(self):
        pass
