from uplogic.nodes import ULConditionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import LOGIC_OPERATORS
from uplogic.utils import is_waiting


class ULCompare(ULConditionNode):
    def __init__(self, operator='GREATER'):
        ULConditionNode.__init__(self)
        self.operator = operator
        self.param_a = None
        self.param_b = None
        self.threshold = None
        self.RESULT = ULOutSocket(self, self.get_result)

    def get_result(self):
        socket = self.get_output('result')
        if socket is None:
            a = self.get_input(self.param_a)
            b = self.get_input(self.param_b)
            threshold = self.get_input(self.threshold)
            operator = self.get_input(self.operator)
            if is_waiting(a, b, threshold):
                return
            if operator > 1:  # eq and neq are valid for None
                if a is None:
                    return
                if b is None:
                    return
            if threshold is None:
                threshold = 0
            if threshold > 0 and abs(a - b) < threshold:
                a = b
            if operator is None:
                return
            return self.set_output(
                'result',
                LOGIC_OPERATORS[operator](a, b)
            )
        return socket

    def evaluate(self):
        self._set_ready()
