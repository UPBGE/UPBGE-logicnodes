from uplogic.nodes import GEConditionNode
from uplogic.nodes import STATUS_READY


class GEOnInit(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)
        self._set_status(STATUS_READY)
        self._value = True

    def reset(self):
        self._value = False

    def evaluate(self):
        pass
