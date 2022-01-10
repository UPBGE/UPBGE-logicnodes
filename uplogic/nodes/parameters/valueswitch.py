from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket


class ULValueSwitch(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.conditon = None
        self.val_a = None
        self.val_b = None
        self.out_value = False
        self.VAL = ULOutSocket(self, self._get_out_value)

    def _get_out_value(self):
        condition = self.get_input(self.condition)
        val_a = self.get_input(self.val_a)
        val_b = self.get_input(self.val_b)
        return (
            val_a if condition is True else val_b
        )

    def evaluate(self):
        self._set_ready()
