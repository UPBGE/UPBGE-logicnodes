from uplogic.nodes import ULConditionNode
from uplogic.utils import STATUS_READY


class ULOnUpdate(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self._set_status(STATUS_READY)
        self._value = True

    def reset(self):
        self._value = True

    def evaluate(self):
        pass
